import json
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, List

from pipes_and_filters.pipes_and_filters import Filter, Repository


# =====================================================
# Prompt
# =====================================================

def build_refactor_prompt(
    repo_name: str,
    tactic: dict,
    repo_tree: str,
    repo_files: dict[str, str],
    applied_steps: List[dict],
    current_phase: str,  # 'RED' or 'GREEN'
    test_results: dict   # {'success': bool, 'stdout': str, 'stderr': str}
) -> str:
    # Извлекаем подробности ошибки для фазы GREEN
    error_context = ""
    if current_phase == "GREEN" and not test_results.get("success"):
        stdout = test_results.get("stdout", "")
        stderr = test_results.get("stderr", "")
        # Берем последние 30 строк, чтобы не раздувать контекст, но видеть суть
        error_logs = (stdout + stderr).splitlines()[-30:]
        error_context = "\n".join(error_logs)

    phase_instr = (
        f"PHASE: RED (Test Creation). \n"
        f"Your goal: Create a NEW pytest file (e.g., 'tests/test_tactic.py') that FAILS. "
        f"The test MUST define the expected behavior for: {tactic.get('Tactic_Name')}."
        if current_phase == "RED" else
        f"PHASE: GREEN (Implementation). \n"
        f"Your goal: Modify the code to make the tests PASS. \n"
        f"CRITICAL: Examine the test failure below and fix the specific cause:\n"
        f"--- TEST FAILURE LOGS ---\n{error_context}\n-------------------------"
    )

    return f"""You are a TDD Python Specialist. Use Pytest style.
Tactic: {json.dumps(tactic, indent=2)}

{phase_instr}

Current Repository State:
{repo_tree}

File Contents:
{"".join(f"\n--- {path} ---\n{content}\n" for path, content in repo_files.items())}

Work History: 
{json.dumps(applied_steps, indent=2)}

STRICT RULES:
1. One change per turn. If a file exists, use "action": "modify_file".
2. In GREEN phase, DO NOT create empty files. Write the actual logic to fix the FAILURES shown above.
3. If you see 'ModuleNotFoundError', it means you forgot to add logic to a file or didn't create it.
4. If ALL tests pass and the tactic is fully implemented, return "action": "STOP".
5. Use 'assert' for Pytest. No 'unittest.TestCase'.

Response must be ONLY JSON:
{{
  "action": "modify_file" | "create_file" | "STOP",
  "path": "relative/path.py",
  "content": "FULL FILE CONTENT",
  "thought": "Analysis of the error and plan to fix it"
}}
"""

# =====================================================
# Memory model
# =====================================================

@dataclass
class AppliedStep:
    iteration: int
    action: str
    path: Optional[str]
    summary: str

    def to_prompt_dict(self) -> dict:
        return {
            "iteration": self.iteration,
            "action": self.action,
            "path": self.path,
            "summary": self.summary,
        }


# =====================================================
# Agent
# =====================================================
class ArchitecturalTacticImplementationAgent(Filter):
    name = "tactic_implementation"

    def __init__(
        self,
        call_llm,
        model_name: str,
        artifacts_dir: Path,
        repo_root: Path,
        max_iterations: int = 5,
    ):
        super().__init__()
        self.call_llm = call_llm
        self.model_name = model_name
        self.artifacts_dir = artifacts_dir
        self.repo_root = repo_root
        self.max_iterations = max_iterations

        self.prompts_root = (
                Path("./experiment/prompts")
                / f"prompt_{self.artifacts_dir.name}.md"
        )
        self.prompts_root.mkdir(parents=True, exist_ok=True)

    # -------------------------------------------------
    # Pipeline entry
    # -------------------------------------------------

    def process(self, repos: List[Repository]) -> List[Repository]:
        for repo in repos:
            self._process_repo(repo)
        return repos

    # -------------------------------------------------
    # Core loop
    # -------------------------------------------------
    def _process_repo(self, repo: Repository) -> None:
        tactic = self._load_selected_tactic(repo)
        if not tactic: return

        repo_path = self.repo_root / repo.name

        if not self._ensure_pytest_installed(repo_path):
            self.logger.error(f"Failed to setup testing environment for {repo.name}")
            return

        applied_steps: List[AppliedStep] = []
        current_phase = "RED"

        test_results = ""

        for iteration in range(self.max_iterations):
            step = self._ask_llm_for_step(repo, tactic, applied_steps, current_phase, test_results)
            if step["action"] == "STOP": break

            test_results = self._apply_step(repo_path, step)

            if current_phase == "RED":
                if not test_results["success"]:
                    self.logger.info("RED Phase OK: Test failed as expected.")
                    current_phase = "GREEN"
                else:
                    self.logger.warning("RED Phase Fail: Test passed immediately.")
            else:  # GREEN
                if test_results["success"]:
                    self.logger.info("GREEN Phase OK: Tests passed.")
                    current_phase = "RED"
                else:
                    self.logger.warning("GREEN Phase Fail: Tests still failing.")

            applied_steps.append(
                AppliedStep(
                    iteration=iteration,
                    action=step["action"],
                    path=step.get("path"),
                    summary=f"[{current_phase}] {step.get('thought', '')}",
                )
            )

    # -------------------------------------------------
    # LLM interaction
    # -------------------------------------------------

    def _ask_llm_for_step(self, repo, tactic, applied_steps, current_phase, test_result) -> dict:
        prompt = build_refactor_prompt(
            repo_name=repo.name,
            tactic=tactic,
            repo_tree=repo.repo_tree,
            repo_files=repo.repo_files,
            applied_steps=[s.to_prompt_dict() for s in applied_steps],
            current_phase=current_phase,
            test_results=test_result
        )

        try:
            response = self.call_llm(prompt, model=self.model_name)

            return self._extract_step_from_llm_response(response)
        except Exception as e:
            self.logger.error(f"LLM call failed: {e}")
            return {"action": "STOP"}

    def _extract_step_from_llm_response(self, response: str) -> dict:
        if not response:
            return {"action": "STOP"}

        # Быстро отсекаем всё ДО первого {
        start = response.find("{")
        if start == -1:
            return {"action": "STOP"}

        candidate = response[start:]

        # Обрезаем всё ПОСЛЕ последней }
        end = candidate.rfind("}")
        if end == -1:
            return {"action": "STOP"}

        candidate = candidate[: end + 1]

        try:
            data = json.loads(candidate)
            if isinstance(data, dict):
                return data
        except json.JSONDecodeError as e:
            self.logger.error(f"JSON decode failed: {e}")

        return {"action": "STOP"}

    # -------------------------------------------------
    # Validation
    # -------------------------------------------------

    def _validate_step(self, step: dict) -> bool:
        action = step.get("action")

        if action == "STOP":
            return True

        if action not in {"modify_file", "create_file"}:
            return False

        path = step.get("path")
        content = step.get("content")

        if not path or not content:
            return False

        if Path(path).name == "__init__.py":
            return False

        # защита от слишком больших изменений
        if content.count("\n") > 400:
            return False

        return True

    # -------------------------------------------------
    # Step application
    # -------------------------------------------------

    def _ensure_pytest_installed(self, repo_path: Path) -> bool:
        self.logger.info("Ensuring pytest is installed...")
        try:
            subprocess.run(["pip", "install", "pytest"], check=True, capture_output=True)
            self._install_requirements(repo_path)
            return True
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Pip installation failed: {e.stderr}")
            return False

    def _apply_step(self, repo_path: Path, step: dict) -> dict:
        action = step["action"]
        path = repo_path / step["path"]
        content = step["content"]

        if action == "create_file":
            path.parent.mkdir(parents=True, exist_ok=True)

        path.write_text(content, encoding="utf-8")
        self.logger.info(f"Applied {action} to {step['path']}")

        return self._run_tests(repo_path)


    def _run_tests(self, repo_path: Path) -> dict:
        result = subprocess.run(
            ["pytest", "-v"],
            cwd=repo_path,
            capture_output=True,
            text=True,
        )
        return {
            "success": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr,
        }

    # -------------------------------------------------
    # Infrastructure
    # -------------------------------------------------

    def _install_requirements(self, repo_path: Path) -> bool:
        req = repo_path / "requirements.txt"
        if not req.exists():
            return True

        result = subprocess.run(
            ["pip", "install", "-r", "requirements.txt"],
            cwd=repo_path,
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            self.logger.error(result.stderr)
            return False

        return True

    # -------------------------------------------------
    # Artifacts
    # -------------------------------------------------

    def _save_artifacts(
        self,
        artifact_dir: Path,
        iteration: int,
        step: dict,
        test_result: dict,
    ) -> None:
        (artifact_dir / f"step_{iteration}.json").write_text(
            json.dumps(step, indent=2),
            encoding="utf-8",
        )
        (artifact_dir / f"test_{iteration}.json").write_text(
            json.dumps(test_result, indent=2),
            encoding="utf-8",
        )

    # -------------------------------------------------
    # Tactic loading
    # -------------------------------------------------

    def _load_selected_tactic(self, repo: Repository) -> Optional[dict]:
        path = (
            self.artifacts_dir
            / f"ai_analysis_{self.model_name.split(':')[0]}"
            / "architecture_tactics"
            / f"{repo.name}.json"
        )

        if not path.exists():
            return None

        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except Exception as e:
            self.logger.error(f"Failed to load tactic: {e}")
            return None

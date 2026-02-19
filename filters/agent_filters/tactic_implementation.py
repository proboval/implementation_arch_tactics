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
) -> str:
    return f"""
You are an automated refactoring agent.

You work on an EXISTING Python repository.
Your goal is to APPLY the given architectural tactic
using SAFE, INCREMENTAL, LOCAL changes.

Repository:
{repo_name}

====================
Repository structure
====================
{repo_tree}

====================
Relevant file excerpts
====================
{"".join(
    f"\n--- {path} ---\n{content}\n"
    for path, content in repo_files.items()
)}

====================
Architectural tactic
====================
{json.dumps(tactic, indent=2)}

====================
Already applied changes
====================
{json.dumps(applied_steps, indent=2)}

====================
Rules (STRICT)
====================
- Propose EXACTLY ONE change
- Modify ONLY ONE file
- The change must be SMALL and LOCAL
- Prefer refactoring over new code
- Do NOT redesign architecture
- Do NOT introduce new abstractions
- If no safe change exists → STOP

- If modifying a large file:
  - Return the FULL file content
  - Ensure the JSON object is COMPLETE and CLOSED
  - Do NOT truncate the response


====================
Output format (CRITICAL)
====================
Return EXACTLY ONE JSON OBJECT.
NO explanations.
NO code fences.
NO additional text.
The response MUST end with a single closing brace `}}`.
Nothing is allowed after it.


Schema:
{{
  "action": "modify_file" | "create_file" | "STOP",
  "path": "relative/path.py",
  "content": "FULL file content (omit only if action=STOP)"
}}

If no change is safe:
{{ "action": "STOP" }}
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
        if not tactic:
            self.logger.info(f"{repo.name}: no tactic selected")
            return

        if not repo.repo_tree or not repo.repo_files:
            self.logger.error(f"{repo.name}: missing repo_tree or repo_files")
            return

        repo_path = self.repo_root / repo.name

        # if not self._install_requirements(repo_path):
        #     self.logger.error(f"{repo.name}: dependency installation failed")
        #     return

        artifact_dir = self.artifacts_dir / "tactic_application" / repo.name
        artifact_dir.mkdir(parents=True, exist_ok=True)

        applied_steps: List[AppliedStep] = []

        for iteration in range(self.max_iterations):
            step = self._ask_llm_for_step(repo, tactic, applied_steps)

            if step["action"] == "STOP":
                self.logger.info(f"{repo.name}: STOP requested")
                break

            if not self._validate_step(step):
                self.logger.warning(f"{repo.name}: invalid step proposed, stopping")
                break

            self._apply_step(repo_path, step)

            applied_steps.append(
                AppliedStep(
                    iteration=iteration,
                    action=step["action"],
                    path=step.get("path"),
                    summary=f"{step['action']} {step.get('path')}",
                )
            )

            self._save_artifacts(
                artifact_dir=artifact_dir,
                iteration=iteration,
                step=step,
                test_result=[],
            )

            # if not test_result["success"]:
            #     self.logger.warning(f"{repo.name}: tests failed")

    # -------------------------------------------------
    # LLM interaction
    # -------------------------------------------------

    def _ask_llm_for_step(
        self,
        repo: Repository,
        tactic: dict,
        applied_steps: List[AppliedStep],
    ) -> dict:
        prompt = build_refactor_prompt(
            repo_name=repo.name,
            tactic=tactic,
            repo_tree=repo.repo_tree,
            repo_files=repo.repo_files,
            applied_steps=[s.to_prompt_dict() for s in applied_steps],
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

    def _apply_step(self, repo_path: Path, step: dict) -> None:
        action = step["action"]
        path = repo_path / step["path"]
        content = step["content"]

        if action == "create_file":
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
            self.logger.info(f"Created file: {path}")
            return

        if action == "modify_file":
            if not path.exists():
                self.logger.error(f"File not found: {path}")
                return
            path.write_text(content, encoding="utf-8")
            self.logger.info(f"Modified file: {path}")

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

    def _run_tests(self, repo_path: Path) -> dict:
        result = subprocess.run(
            ["pytest"],
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

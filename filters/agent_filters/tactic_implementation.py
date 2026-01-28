import json
import shutil
import subprocess
from pathlib import Path
from pipes_and_filters.pipes_and_filters import Filter


def build_refactor_prompt(
    repo_name: str,
    tactic: dict,
    repo_tree: str,
    repo_files: dict[str, str],
    previous_steps: list[dict],
):
    return f"""
You are a senior backend engineer strictly following Test Driven Development (TDD).

You are working inside an EXISTING real Python repository.

Repository name:
{repo_name}

========================================
REPOSITORY FILE STRUCTURE
========================================
{repo_tree}

========================================
FULL FILE CONTENTS (only signatures and imports)
========================================
{"".join(
    f"\n--- FILE: {path} ---\n{content}\n"
    for path, content in repo_files.items()
)}

========================================
SELECTED ARCHITECTURAL TACTIC
========================================
{json.dumps(tactic, indent=2)}

========================================
PREVIOUS TDD STEPS
========================================
{json.dumps(previous_steps, indent=2) if previous_steps else "No steps yet."}

========================================
STRICT DEVELOPMENT PROCESS (MANDATORY)
========================================
You MUST follow Test Driven Development:

Iteration rules:
1. FIRST create or modify a TEST that describes the next desired behavior
2. The test MUST fail on current code
3. THEN implement the MINIMAL production code needed to pass the test
4. NEVER implement production code without a test
5. ONE SMALL CHANGE per iteration
6. If the tactic is fully implemented, respond with STOP

========================================
CONSTRAINTS (STRICT)
========================================
- Do NOT break existing tests
- Do NOT rewrite large components
- Prefer refactoring over new abstractions
- Avoid touching unrelated files
- If unsure, respond with STOP

========================================
OUTPUT FORMAT (STRICT)
========================================
Return ONLY valid JSON.
The JSON MUST be an ARRAY of steps.

Each step MUST follow EXACTLY this schema:

{{
  "action": one of [
    "create_file",
    "modify_file",
    "STOP"
  ],
  "path": "relative/path",
  "content": "file content if applicable"
}}

Rules:
- Test steps MUST target test files (tests/, *_test.py, test_*.py)
- Implementation steps MUST target production code
- NEVER mix test and implementation in the same step
- NEVER output more than ONE step per response
- DO NOT include explanations
- DO NOT include markdown
- DO NOT modify __init__.py files
- Backend code only

If no safe next TDD step exists:
[
  {{ "action": "STOP" }}
]

IMPORTANT:
- First response MUST be a TEST
- There is NO NEED to finish the whole tactic
- Stop as soon as the tactic is sufficiently covered by tests
"""


class ArchitecturalTacticImplementationAgent(Filter):
    name = "tacticImplementation"

    def __init__(self, call_llm, model_name: str, artifacts_dir: Path, max_iterations: int = 5):
        super().__init__()
        self.call_llm = call_llm
        self.artifacts_dir = artifacts_dir
        self.max_iterations = max_iterations
        self.model_name = model_name

    # -------------------------------------------------
    # Pipeline entrypoint
    # -------------------------------------------------
    def process(self, repos):
        if not repos:
            self.logger.warning("No repositories passed to tactic implementation stage")
            return repos or []

        for repo in repos:
            try:
                self.apply_tactic(repo)
            except Exception as e:
                self.logger.error(f"Unexpected error for repo {repo.name}: {e}")

        return repos

    # -------------------------------------------------
    # Main tactic loop
    # -------------------------------------------------
    def apply_tactic(self, repo):
        tactic = self.load_selected_tactic(repo)
        if not tactic:
            self.logger.warning(f"No selected tactic for {repo.name}")
            return

        if not hasattr(repo, "repo_tree") or not hasattr(repo, "repo_files"):
            self.logger.error(
                f"Repository context missing for {repo.name} "
                f"(repo_tree / repo_files not found)"
            )
            return

        repo_path = self.artifacts_dir / "repos" / repo.name

        if not self.install_requirements(repo_path):
            self.logger.error(
                f"Skipping repo {repo.name} due to dependency installation failure"
            )
            return

        artifact_dir = (
            self.artifacts_dir / "tactic_application" / repo.name
        )
        artifact_dir.mkdir(parents=True, exist_ok=True)

        applied_steps_summary = []

        for iteration in range(self.max_iterations):
            steps = self.ask_llm_for_steps(repo, tactic, applied_steps_summary)

            if not steps:
                break

            step = steps[0]
            action = step.get("action", "STOP")

            if action == "STOP":
                self.logger.info("LLM requested STOP")
                return

            self.apply_step(repo_path, step)

            test_result = self.run_tests(repo_path)
            self.save_step(artifact_dir, iteration, step, test_result)

            applied_steps_summary.append({
                "iteration": iteration,
                "action": action,
                "path": step.get("path"),
                "tests_passed": test_result["success"],
            })

            if not test_result["success"]:
                self.logger.info("Tests failed (expected for TDD), continuing")
                continue


    def install_requirements(self, repo_path: Path) -> bool:
        req = repo_path / "requirements.txt"
        if not req.exists():
            self.logger.info("No requirements.txt found, skipping dependency install")
            return True

        self.logger.info(f"Installing dependencies for {repo_path.name}")

        result = subprocess.run(
            [
                "pip",
                "install",
                "-r",
                "requirements.txt",
            ],
            cwd=repo_path,
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            self.logger.error(
                f"Dependency installation failed:\n{result.stderr}"
            )
            return False

        return True

    # -------------------------------------------------
    # LLM interaction
    # -------------------------------------------------
    def ask_llm_for_steps(self, repo, tactic, applied_steps_summary):
        prompt = build_refactor_prompt(
            repo.name,
            tactic,
            repo.repo_tree,
            repo.repo_files,
            applied_steps_summary
        )

        try:
            response = self.call_llm(prompt, model=self.model_name)
            data = json.loads(response)
        except Exception as e:
            self.logger.error(f"Failed to parse LLM response: {e}")
            return []

        if not isinstance(data, list):
            self.logger.error("LLM response is not a list, ignoring")
            return []

        return data

    # -------------------------------------------------
    # Artifact loading
    # -------------------------------------------------
    def load_selected_tactic(self, repo):
        path = (
            self.artifacts_dir
            / f"ai_analysis_{self.model_name.split(":")[0]}"
            / "architecture_tactics"
            / f"{repo.name}.json"
        )

        if not path.exists():
            return None

        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except Exception as e:
            self.logger.error(f"Failed to load tactic for {repo.name}: {e}")
            return None

    # -------------------------------------------------
    # Step application
    # -------------------------------------------------
    def apply_step(self, repo_path: Path, step: dict):
        action = step.get("action")

        handlers = {
            "create_directory": self.create_directory,
            "create_file": self.create_file,
            "modify_file": self.modify_file,
            "move_file": self.move_file,
            "delete_file": self.delete_file,
        }

        handler = handlers.get(action)

        if not handler:
            self.logger.error(f"Unknown action '{action}', skipping step")
            return

        handler(repo_path, step)

    # -------------------------------------------------
    # Actions
    # -------------------------------------------------
    def create_directory(self, repo_path: Path, step: dict):
        path = repo_path / step.get("path", "")
        if not path:
            return
        path.mkdir(parents=True, exist_ok=True)
        self.logger.info(f"Created directory: {path}")

    def create_file(self, repo_path: Path, step: dict):
        path = repo_path / step.get("path", "")
        content = step.get("content", "")

        if not path:
            return

        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        self.logger.info(f"Created file: {path}")

    def modify_file(self, repo_path: Path, step: dict):
        path = repo_path / step.get("path", "")
        content = step.get("content")

        if not path or content is None:
            self.logger.error("modify_file requires path and content")
            return

        if not path.exists():
            self.logger.error(f"File does not exist: {path}")
            return

        path.write_text(content, encoding="utf-8")
        self.logger.info(f"Modified file: {path}")

    def move_file(self, repo_path: Path, step: dict):
        src = repo_path / step.get("from", "")
        dst = repo_path / step.get("path", "")

        if not src.exists():
            self.logger.error(f"Source file not found: {src}")
            return

        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(src), str(dst))
        self.logger.info(f"Moved file: {src} -> {dst}")

    def delete_file(self, repo_path: Path, step: dict):
        path = repo_path / step.get("path", "")

        if not path.exists():
            self.logger.warning(f"File to delete not found: {path}")
            return

        path.unlink()
        self.logger.info(f"Deleted file: {path}")

    # -------------------------------------------------
    # Testing & rollback
    # -------------------------------------------------
    def run_tests(self, repo_path: Path):
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

    def rollback(self, repo_path: Path, repo_name: str):
        snapshot = self.artifacts_dir / "snapshots" / repo_name / "baseline"

        if not snapshot.exists():
            self.logger.error("No snapshot found, cannot rollback")
            return

        self.logger.warning(f"Rolling back repo {repo_name} to baseline snapshot")

        shutil.rmtree(repo_path, ignore_errors=True)
        shutil.copytree(snapshot, repo_path)

    # -------------------------------------------------
    # Artifacts
    # -------------------------------------------------
    def save_step(self, out_dir: Path, idx: int, step: dict, test_result: dict):
        out_dir.mkdir(parents=True, exist_ok=True)

        (out_dir / f"step_{idx}.json").write_text(
            json.dumps(step, indent=2), encoding="utf-8"
        )

        (out_dir / f"test_{idx}.json").write_text(
            json.dumps(test_result, indent=2), encoding="utf-8"
        )

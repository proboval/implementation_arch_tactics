import json
import shutil
import subprocess
from pathlib import Path
from pipes_and_filters.pipes_and_filters import Filter

class ArchitecturalTacticImplementationAgent(Filter):
    name = "tacticImplementation"

    def __init__(self, call_llm, artifacts_dir: Path, max_iterations=5):
        super().__init__()
        self.call_llm = call_llm
        self.artifacts_dir = artifacts_dir
        self.max_iterations = max_iterations

    def process(self, repos):
        """
        Основной метод фильтра.
        Пробегает по всем репозиториям и пытается применить выбранную тактику.
        """
        for repo in repos:
            self.apply_tactic(repo)
        return repos

    # ---------------------------
    # Основной цикл применения тактики
    # ---------------------------
    def apply_tactic(self, repo):
        tactic = self.load_selected_tactic(repo)
        repo_path = Path("artifacts/repos") / repo.name
        tactic_artifact_dir = self.artifacts_dir / "tactic_application" / repo.name
        tactic_artifact_dir.mkdir(parents=True, exist_ok=True)

        for iteration in range(self.max_iterations):
            # Получаем микро-шаг от LLM
            plan = self.ask_llm_for_next_step(repo, tactic)

            self.logger.info(f"PLAN | {plan} | {type(plan)}")

            action = plan.get("action", "STOP")

            if action == "STOP":
                self.logger.info("Tactic execution finished")
                break

            self.apply_change(repo_path, plan)

            test_result = self.run_tests(repo_path)

            self.save_step(tactic_artifact_dir, iteration, plan, test_result)

            if not test_result["success"]:
                # Если тесты упали — откатываем изменения и прекращаем
                self.rollback(repo_path)
                self.log_failure(repo_path, plan, test_result)
                break

    # ---------------------------
    # Методы LLM и работы с планом
    # ---------------------------
    def load_selected_tactic(self, repo):
        """
        Загружает выбранную тактику для репозитория из артефактов.
        """
        path = self.artifacts_dir / "ai_analysis" / "architecture_tactics" / f"{repo.name}.json"
        return json.loads(path.read_text())

    def ask_llm_for_next_step(self, repo, tactic):
        """
        Запрашивает у LLM следующий микро-шаг внедрения тактики.
        Возвращает dict:
        {
            "action": "...",
            "rationale": "...",
            "files": [...],
            "risk": "low|medium|high"
        }
        """
        prompt = f"""
You are a software architecture refactoring assistant.

Selected architectural tactic:
{json.dumps(tactic, indent=2)}

Project context: {repo.name}

Constraints:
- Make ONE small, reversible change
- Do NOT break existing tests
- Prefer refactoring over rewriting
- If risky, respond with STOP

Return STRICT JSON.

Each step MUST follow this schema:

{{
  "action": one of [
    "create_directory",
    "create_file",
    "modify_file",
    "move_file",
    "delete_file", 
    "STOP"
  ],
  "path": "relative/path",
  "content": "file content if applicable",
  "from": "old path (only for move_file)"
}}

DO NOT invent new action names.
DO NOT use natural language as action.
"""
        response = self.call_llm(prompt)
        return json.loads(response)

    def apply_change(self, repo_path: Path, plan: dict):
        """
        Применяет микро-шаг к репозиторию.
        """
        action = plan["action"]
        files = plan.get("files", [])

        handlers = {
            "create_directory": self.create_directory,
            "create_file": self.create_file,
            "modify_file": self.modify_file,
            "move_file": self.move_file,
            "delete_file": self.delete_file,
        }

        handler = handlers.get(action)

        if not handler:
            raise ValueError(f"Unknown action: {action}")

        handler(repo_path, plan)

    # ---------------------------
    # Тестирование и откат
    # ---------------------------
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

    def rollback(self, repo_path: Path):
        subprocess.run(["git", "checkout", "."], cwd=repo_path)

    # ---------------------------
    # Логирование и сохранение артефактов
    # ---------------------------
    def save_step(self, out_dir: Path, step_idx: int, plan: dict, test_result: dict):
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / f"plan_step_{step_idx}.json").write_text(json.dumps(plan, indent=2))
        (out_dir / f"test_result_step_{step_idx}.json").write_text(json.dumps(test_result, indent=2))

    def log_failure(self, repo_path: Path, plan: dict, test_result: dict):
        print(f"[FAILURE] Repo: {repo_path}, Plan: {plan['action']}, Risk: {plan.get('risk')}")
        print(f"Test stdout: {test_result['stdout']}")
        print(f"Test stderr: {test_result['stderr']}")

    def create_directory(self, repo_path: Path, step: dict):
        path = repo_path / step["path"]
        path.mkdir(parents=True, exist_ok=True)
        self.logger.info(f"Created directory: {path}")

    def create_file(self, repo_path: Path, step: dict):
        path = repo_path / step["path"]
        content = step.get("content", "")

        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

        self.logger.info(f"Created file: {path}")

    def modify_file(self, repo_path: Path, step: dict):
        path = repo_path / step["path"]
        content = step.get("content")

        if not path.exists():
            raise FileNotFoundError(f"Cannot modify missing file: {path}")

        if content is None:
            raise ValueError("modify_file requires 'content'")

        path.write_text(content, encoding="utf-8")
        self.logger.info(f"Modified file: {path}")

    def move_file(self, repo_path: Path, step: dict):
        src = repo_path / step["from"]
        dst = repo_path / step["path"]

        if not src.exists():
            raise FileNotFoundError(f"Source file not found: {src}")

        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(src), str(dst))

        self.logger.info(f"Moved file: {src} -> {dst}")

    def delete_file(self, repo_path: Path, step: dict):
        path = repo_path / step["path"]

        if not path.exists():
            self.logger.warning(f"File already missing: {path}")
            return

        if path.is_dir():
            shutil.rmtree(path)
        else:
            path.unlink()

        self.logger.info(f"Deleted: {path}")

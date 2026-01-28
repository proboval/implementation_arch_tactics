import csv
import shutil
import subprocess
from pathlib import Path
from typing import List

from pipes_and_filters.pipes_and_filters import Filter
from pipes_and_filters.pipes_and_filters import Repository


ML_KEYWORDS = {
    "torch",
    "tensorflow",
    "sklearn",
    "scikit-learn",
    "keras",
    "xgboost",
    "lightgbm",
    "catboost",
    "transformers",
    "langchain",
    "llama",
    "openai",
}

EXCLUDED_DIRS = {
    "notebooks",
    "experiments",
    "examples",
    "ml",
    "ai",
}


class BackendDatasetPreparationFilter(Filter):
    name = "backend_dataset_preparation"

    def __init__(
        self,
        workdir: Path,
        output_csv: Path,
        max_repos: int | None = None,
    ):
        super().__init__()
        self.workdir = workdir
        self.output_csv = output_csv
        self.max_repos = max_repos

        self.workdir.mkdir(parents=True, exist_ok=True)

    def process(self, repositories: List[Repository]):
        backend_repos: List[Repository] = []

        for idx, repo in enumerate(repositories):
            if self.max_repos and idx >= self.max_repos:
                break

            try:
                if self.process_repo(repo):
                    backend_repos.append(repo)
            except Exception as e:
                self.logger.error(f"Failed processing {repo.full_name}: {e}")

        self.write_csv(backend_repos)
        return backend_repos

    def process_repo(self, repo: Repository) -> bool:
        repo_path = self.workdir / repo.name

        self.clone_repo(repo.url, repo_path)
        repo.local_path = repo_path

        try:
            is_backend = self.is_backend_repo(repo_path)
        finally:
            shutil.rmtree(repo_path, ignore_errors=True)
            repo.local_path = None
            repo.repo_files = None
            repo.repo_tree = None

        if is_backend:
            self.logger.info(f"[BACKEND] {repo.full_name}")
        else:
            self.logger.info(f"[SKIP] {repo.full_name}")

        return is_backend

    def clone_repo(self, url: str, path: Path):
        subprocess.run(
            ["git", "clone", "--depth", "1", url, str(path)],
            capture_output=True,
            text=True,
            check=False,
        )

    def is_backend_repo(self, repo_path: Path) -> bool:
        # 1. requirements.txt
        req = repo_path / "requirements.txt"
        if not req.exists():
            return False

        req_text = req.read_text(encoding="utf-8", errors="ignore").lower()

        if any(kw in req_text for kw in ML_KEYWORDS):
            return False

        # 2. python files
        py_files = list(repo_path.rglob("*.py"))
        if not py_files:
            return False

        # 3. exclude dirs
        for p in py_files:
            if any(part.lower() in EXCLUDED_DIRS for part in p.parts):
                return False

        return True

    def write_csv(self, repos: List[Repository]):
        self.output_csv.parent.mkdir(parents=True, exist_ok=True)

        with self.output_csv.open("w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["name", "clone_url"])

            for repo in repos:
                writer.writerow([repo.full_name, repo.url])

        self.logger.info(
            f"Saved {len(repos)} backend repositories to {self.output_csv}"
        )

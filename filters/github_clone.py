import subprocess
from pathlib import Path
from typing import Iterable, List
from pipes_and_filters.pipes_and_filters import Filter, Repository
import shutil


class CloneRepositoriesFilter(Filter):
    name = "cloneRepositories"

    def __init__(
        self,
        base_dir: Path,
        artifacts_dir: Path
    ):
        super().__init__()
        self.base_dir = base_dir
        self.artifacts_dir = artifacts_dir

        self.base_dir.mkdir(parents=True, exist_ok=True)
        self.artifacts_dir.mkdir(parents=True, exist_ok=True)

    def process(self, data: Iterable[Repository]) -> List[Repository]:
        results = []

        for repo in data:
            repo_dir = self.base_dir / repo.name

            if repo_dir.exists():
                repo.local_path = repo_dir
            else:
                try:
                    subprocess.run(
                        ["git", "clone", repo.url, str(repo_dir)],
                        check=True,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True,
                    )
                    repo.local_path = repo_dir
                    self.init_snapshot(repo.local_path, repo.name)

                except subprocess.CalledProcessError as e:
                    repo.local_path = None
                    repo.metadata = repo.metadata or {}
                    repo.metadata["clone_error"] = e.stderr

            results.append(repo)

        return results

    def init_snapshot(self, repo_path: Path, repo_name: str):
        """
        Create baseline snapshot of repository for rollback.
        Snapshot is created only once.
        """

        snapshot_root = self.artifacts_dir / "snapshots" / repo_name
        baseline_snapshot = snapshot_root / "baseline"

        if baseline_snapshot.exists():
            self.logger.info(
                f"Snapshot already exists for {repo_name}, skipping initialization"
            )
            return

        try:
            snapshot_root.mkdir(parents=True, exist_ok=True)

            self.logger.info(
                f"Creating baseline snapshot for {repo_name}"
            )

            shutil.copytree(
                repo_path,
                baseline_snapshot,
                ignore=shutil.ignore_patterns(
                    ".git",
                    "__pycache__",
                    "*.pyc",
                    ".pytest_cache",
                    ".mypy_cache",
                    ".venv",
                ),
            )

            self.logger.info(
                f"Baseline snapshot created for {repo_name}"
            )

        except Exception as e:
            self.logger.error(
                f"Failed to create snapshot for {repo_name}: {e}"
            )


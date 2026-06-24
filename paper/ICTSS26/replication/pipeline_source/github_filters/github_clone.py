import subprocess
from pathlib import Path
from typing import Iterable, List
from pipes_and_filters.pipes_and_filters import Filter, Repository


class CloneRepositoriesFilter(Filter):
    name = "cloneRepositories"

    def __init__(
        self,
        base_dir: Path,
    ):
        super().__init__()
        self.base_dir = base_dir

        self.base_dir.mkdir(parents=True, exist_ok=True)

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

                except subprocess.CalledProcessError as e:
                    repo.local_path = None
                    repo.metadata = repo.metadata or {}
                    repo.metadata["clone_error"] = e.stderr

            results.append(repo)

        return results

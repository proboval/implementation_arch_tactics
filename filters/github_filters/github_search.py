from pathlib import Path
from typing import List, Tuple
import requests
from pipes_and_filters.pipes_and_filters import Filter, Repository


class GitHubSearchFilter(Filter):
    name = "searchRepositories"

    def __init__(
        self,
        token: str,
        output_file: Path,
        max_repos: int = 10,
        repos_base_dir: Path = Path("artifacts/repos"),
        stars: Tuple[int, int] = (100, 1000)
    ):
        super().__init__()
        self.token = token
        self.max_repos = max_repos
        self.output_file = output_file
        self.repos_base_dir = repos_base_dir
        self.stars = stars

        self.output_file.parent.mkdir(parents=True, exist_ok=True)
        self.repos_base_dir.mkdir(parents=True, exist_ok=True)

    def process(self, data=None):
        if self.output_file.exists():
            repos = self._search_exist_repos()
        else:
            repos = self._search_random_repos()

        return repos

    def _search_exist_repos(self) -> List[Repository]:
        headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {self.token}",
            "User-Agent": "get-git-repos/1.0",
        }

        repos: List[Repository] = []

        for line in self.output_file.read_text(encoding="utf-8").splitlines():
            full_name = line.strip()
            if not full_name or full_name.startswith("#"):
                continue

            repo_name = full_name.split("/")[-1]
            local_path = self.repos_base_dir / repo_name

            if local_path.exists():
                self.logger.info(
                    f"Repo {full_name} already cloned, using local data"
                )

                repos.append(
                    Repository(
                        name=repo_name,
                        full_name=full_name,
                        url=f"https://github.com/{full_name}.git",
                        stars=0,
                        forks=0,
                        size_kb=0,
                        language="Python",
                        local_path=local_path,
                    )
                )
            else:
                url = f"https://api.github.com/repos/{full_name}"
                try:
                    response = requests.get(url, headers=headers, timeout=30)
                except Exception as e:
                    self.logger.warning(f"Failed to connect to GitHub for {full_name}: {e}")
                    continue

                if response.status_code != 200:
                    self.logger.warning(
                        f"Failed to load {full_name}: {response.status_code}"
                    )
                    continue

                item = response.json()

                repos.append(
                    Repository(
                        name=item["name"],
                        full_name=item["full_name"],
                        url=item["clone_url"],
                        stars=item.get("stargazers_count", 0),
                        forks=item.get("forks_count", 0),
                        size_kb=item.get("size", 0),
                        language=item.get("language"),
                        local_path=local_path,
                    )
                )

        self._save_paths(repos)
        return repos

    def _search_random_repos(self) -> List[Repository]:
        headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github+json",
            "User-Agent": "get-git-repos/1.0",
        }

        query = (
            "language:Python "
            f"stars:{self.stars[0]}..{self.stars[1]} "
            "forks:>=30 "
            "size:<=5000"
        )

        url = "https://api.github.com/search/repositories"

        repos: List[Repository] = []
        temp_max_repos = self.max_repos
        found_repos = 0

        while temp_max_repos:
            per_page = 100
            if temp_max_repos >= per_page:
                temp_max_repos -= per_page
            else:
                per_page = temp_max_repos
                temp_max_repos = 0

            response = requests.get(
                url,
                headers=headers,
                params={
                    "q": query,
                    "sort": "stars",
                    "order": "desc",
                    "per_page": per_page,
                },
                timeout=30,
            )

            response.raise_for_status()
            items = response.json().get("items", [])

            for item in items:
                repo_name = item["name"]
                local_path = self.repos_base_dir / repo_name

                repos.append(
                    Repository(
                        name=repo_name,
                        full_name=item["full_name"],
                        url=item["clone_url"],
                        stars=item.get("stargazers_count", 0),
                        forks=item.get("forks_count", 0),
                        size_kb=item.get("size", 0),
                        language=item.get("language"),
                        local_path=local_path,
                    )
                )

            found_repos += per_page

            self.logger.info(f"Found {found_repos}/{self.max_repos} repos")

        self._save_paths(repos)
        return repos

    def _save_paths(self, repos: List[Repository]):
        with open(self.output_file, "a", encoding="utf-8") as f:
            for repo in repos:
                f.write(f"{repo.full_name}\n")

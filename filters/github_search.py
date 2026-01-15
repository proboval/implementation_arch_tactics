import requests
from pipes_and_filters.pipes_and_filters import Filter, Repository


class GitHubSearchFilter(Filter):
    name = "searchRepositories"

    def __init__(self, token: str, max_repos: int = 10):
        super().__init__()
        self.token = token
        self.max_repos = max_repos

    def process(self, data=None):
        headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github+json",
        }

        query = (
            "language:Python "
            "stars:100..1000 "
            "forks:>=15 "
            "size:<=2000"
        )

        url = "https://api.github.com/search/repositories"

        response = requests.get(
            url,
            headers=headers,
            params={
                "q": query,
                "sort": "stars",
                "order": "desc",
                "per_page": self.max_repos,
            },
        )

        response.raise_for_status()
        items = response.json()["items"]

        repos = []
        for item in items:
            repos.append(
                Repository(
                    name=item["name"],
                    full_name=item["full_name"],
                    url=item["clone_url"],
                    stars=item["stargazers_count"],
                    forks=item["forks_count"],
                    size_kb=item["size"],
                    language=item["language"],
                )
            )

        return repos

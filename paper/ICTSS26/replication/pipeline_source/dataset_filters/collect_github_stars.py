import csv
import requests
from pathlib import Path
from pipes_and_filters.pipes_and_filters import Filter


class DatasetMergeAndEnrichFilter(Filter):
    """
    Объединяет dataset_*.csv в один dataset.csv
    и дописывает количество звезд репозитория
    """
    name = "dataset_merge_and_enrich"

    def __init__(
        self,
        input_dir: Path,
        output_csv: Path,
        github_token: str | None = None,
    ):
        super().__init__()
        self.input_dir = input_dir
        self.output_csv = output_csv
        self.github_token = github_token

    # -------------------------------------------------
    # Pipeline entrypoint
    # -------------------------------------------------
    def process(self, _):
        repos = self.collect_repos()
        enriched = []

        for repo in repos:
            stars = self.fetch_stars(repo["full_name"])
            enriched.append({
                "full_name": repo["full_name"],
                "clone_url": repo["clone_url"],
                "stars": stars,
            })

        self.write_csv(enriched)
        self.logger.info(
            f"Final dataset written to {self.output_csv}, "
            f"repos count = {len(enriched)}"
        )

        return _

    # -------------------------------------------------
    # Collect input CSVs
    # -------------------------------------------------
    def collect_repos(self) -> list[dict]:
        repos = []
        seen = set()

        for path in self.input_dir.iterdir():
            if not path.name.startswith("dataset_"):
                continue
            if path.suffix != ".csv":
                continue

            self.logger.info(f"Reading {path.name}")

            with path.open(encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    full_name = row.get("full_name")
                    clone_url = row.get("clone_url")

                    if not full_name or not clone_url:
                        continue

                    if full_name in seen:
                        continue

                    seen.add(full_name)
                    repos.append({
                        "full_name": full_name,
                        "clone_url": clone_url,
                    })

        return repos

    # -------------------------------------------------
    # GitHub API
    # -------------------------------------------------
    def fetch_stars(self, full_name: str) -> int:
        """
        full_name = owner/repo
        """
        url = f"https://api.github.com/repos/{full_name}"
        headers = {
            "Accept": "application/vnd.github+json",
        }

        if self.github_token:
            headers["Authorization"] = f"Bearer {self.github_token}"

        try:
            r = requests.get(url, headers=headers, timeout=10)
            if r.status_code != 200:
                self.logger.warning(
                    f"Failed to fetch stars for {full_name}: {r.status_code}"
                )
                return 0

            data = r.json()
            return int(data.get("stargazers_count", 0))

        except Exception as e:
            self.logger.warning(f"Error fetching stars for {full_name}: {e}")
            return 0

    # -------------------------------------------------
    # Output
    # -------------------------------------------------
    def write_csv(self, rows: list[dict]):
        self.output_csv.parent.mkdir(parents=True, exist_ok=True)

        with self.output_csv.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(
                f,
                fieldnames=["full_name", "clone_url", "stars"],
            )
            writer.writeheader()
            writer.writerows(rows)

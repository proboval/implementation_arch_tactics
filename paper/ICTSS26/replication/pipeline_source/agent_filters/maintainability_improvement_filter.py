import csv
import shutil
import subprocess
from pathlib import Path
from typing import List

from pipes_and_filters.pipes_and_filters import Filter, Repository
from filters.help_methods import build_repo_tree, collect_repo_files


class DatasetLLMImprovementRunner(Filter):
    name = "DatasetLLMImprovementRunner"

    def __init__(
        self,
        input_csv: Path,
        output_csv: Path,
        workdir: Path,
        architecture_filter: Filter,
        tactic_filter: Filter,
        implementation_filter: Filter,
        maintainability_filter_factory,
    ):
        super().__init__()
        self.input_csv = input_csv
        self.output_csv = output_csv
        self.workdir = workdir

        self.architecture_filter = architecture_filter
        self.tactic_filter = tactic_filter
        self.implementation_filter = implementation_filter
        self.maintainability_filter_factory = maintainability_filter_factory

        self.workdir.mkdir(parents=True, exist_ok=True)

    def process(self, _: List[Repository]) -> List[Repository]:
        rows = self._read_input_csv()
        self._init_output_csv()

        for row in rows:
            try:
                self._process_repo_row(row)
            except Exception as e:
                self.logger.error(f"Failed {row['full_name']}: {e}")

        return []

    # ---------- CORE FLOW ----------

    def _process_repo_row(self, row: dict):
        repo_name = row["full_name"].split("/")[1]
        clone_url = row["clone_url"]

        repo_path = self.workdir / repo_name

        self._clone_repo(clone_url, repo_path)

        repo = Repository(
            name=row["full_name"],
            full_name=row["full_name"],
            url=clone_url,
            stars=int(row.get("stars", 0)),
            forks=int(row.get("forks", 0)),
            size_kb=int(row.get("size_kb", 0)),
            language=row.get("language", "Python"),
            local_path=repo_path,
            metadata={},
        )

        # наполняем структуру
        repo.repo_tree = build_repo_tree(repo_path)
        repo.repo_files = collect_repo_files(repo_path)

        try:
            # --- maintainability BEFORE ---
            before_filter = self.maintainability_filter_factory("BEFORE")
            before_filter.run([repo])

            repo.name = repo.name.split("/")[1]

            # --- LLM filters ---
            self.architecture_filter.run([repo])
            self.tactic_filter.run([repo])
            self.implementation_filter.run([repo])

            # --- maintainability AFTER ---
            after_filter = self.maintainability_filter_factory("AFTER")
            after_filter.run([repo])

            self._append_result(repo)
        except Exception as e:
            self.logger.error(f"Failed {row['full_name']}: {e}")

        self._cleanup_repo(repo_path)

    # ---------- CSV ----------

    def _read_input_csv(self) -> List[dict]:
        with self.input_csv.open(encoding="utf-8") as f:
            return list(csv.DictReader(f))

    def _init_output_csv(self):
        if self.output_csv.exists():
            return

        with self.output_csv.open("w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                "full_name",
                "clone_url",
                "mi_before",
                "mi_after",
                "architecture_summary",
                "chosen_tactic",
            ])

    def _append_result(self, repo: Repository):
        meta = repo.metadata or {}

        with self.output_csv.open("a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                repo.full_name,
                repo.url,
                meta.get("mi_before"),
                meta.get("mi_after"),
                meta.get("architecture"),
                meta.get("tactic"),
            ])

    # ---------- GIT / FS ----------

    def _clone_repo(self, clone_url: str, repo_path: Path):
        subprocess.run(
            ["git", "clone", "--depth", "1", clone_url, str(repo_path)],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

    def _cleanup_repo(self, repo_path: Path):
        shutil.rmtree(repo_path, ignore_errors=True)

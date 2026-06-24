import csv
import json
import shutil
import subprocess
from pathlib import Path
from typing import Dict

from pipes_and_filters.pipes_and_filters import Filter, Repository


class DatasetMaintainabilityEnricher(Filter):
    name = "dataset_maintainability_enricher"

    def __init__(
        self,
        dataset_csv: Path,
        output_csv: Path,
        artifacts_dir: Path,
        static_analysis_filter: Filter,
        workdir: Path,
    ):
        super().__init__()
        self.dataset_csv = dataset_csv
        self.output_csv = output_csv
        self.artifacts_dir = artifacts_dir
        self.static_analysis_filter = static_analysis_filter
        self.workdir = workdir

    # -------------------------------------------------
    def process(self, _):
        rows = self._read_csv()
        enriched = []

        for row in rows:
            try:
                enriched.append(self._process_repo(row))
            except Exception as e:
                self.logger.error(f"Failed {row['full_name']}: {e}")
                enriched.append(row)

        self._write_csv(enriched)
        return _

    # -------------------------------------------------
    def _process_repo(self, row: Dict[str, str]) -> Dict[str, str]:
        repo_name = row["full_name"]
        clone_url = row["clone_url"]

        repo_path = self.workdir / repo_name.replace("/", "__")

        self._clone_repo(clone_url, repo_path)

        try:
            repo = Repository(
                name=repo_name.split("/")[-1],
                full_name=repo_name,
                url=clone_url,
                stars=int(row.get("stars", 0)),
                forks=0,
                size_kb=0,
                language="Python",
                local_path=repo_path,
            )

            self.static_analysis_filter.run([repo])

            metrics = self._load_metrics(repo.name)

            row.update(metrics)
            return row

        finally:
            shutil.rmtree(repo_path, ignore_errors=True)

    # -------------------------------------------------
    def _load_metrics(self, repo_name: str) -> Dict[str, float]:
        base = (
            self.artifacts_dir
            / "static_analysis"
            / "BEFORE"
            / repo_name
        )

        def load(name):
            p = base / name
            return json.loads(p.read_text()) if p.exists() else {}

        code = load("code_maintainability.json")
        arch = load("architecture_maintainability.json")
        doc = load("documentation_maintainability.json")

        return {
            "mi_avg": code.get("mi_avg", 0),
            "files_analyzed": code.get("files_analyzed", 0),
            "packages": arch.get("packages", 0),
            "avg_fan_out": arch.get("avg_fan_out", 0),
            "docstring_coverage": doc.get("docstring_coverage", 0),
            "has_readme": doc.get("has_readme", False),
        }

    # -------------------------------------------------
    def _clone_repo(self, url: str, path: Path):
        subprocess.run(
            ["git", "clone", "--depth", "1", url, str(path)],
            check=True,
            capture_output=True,
        )

    # -------------------------------------------------
    def _read_csv(self):
        with self.dataset_csv.open(encoding="utf-8") as f:
            return list(csv.DictReader(f))

    def _write_csv(self, rows):
        if not rows:
            return

        with self.output_csv.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)

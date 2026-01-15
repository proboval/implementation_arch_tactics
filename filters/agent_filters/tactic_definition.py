import csv
import json
from pathlib import Path
from pipes_and_filters.pipes_and_filters import Filter


TACTICS_CATALOG_PATH = Path("architectural_tactics_complete_catalog.csv")


class ArchitectureTacticSelectionFilter(Filter):
    name = "architecture_tactic_selection"

    def __init__(
        self,
        artifacts_dir: Path,
        tactics_catalog: Path,
        call_llm
    ):
        super().__init__()
        self.artifacts_dir = artifacts_dir
        self.tactics_catalog = tactics_catalog
        self.tactics = self._load_tactics()
        self.call_llm = call_llm

        self.architecture_dir = (
            self.artifacts_dir / "ai_analysis" / "architecture"
        )
        self.static_analysis_dir = (
            self.artifacts_dir / "static_analysis" / "BEFORE"
        )
        self.output_dir = (
            self.artifacts_dir / "ai_analysis" / "architecture_tactics"
        )
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def _load_tactics(self):
        with open(self.tactics_catalog, encoding="utf-8") as f:
            return list(csv.DictReader(f))

    def process(self, repositories: list):
        for repo in repositories:
            repo_name = repo.name

            self.logger.info(f"Selecting tactic for repo: {repo_name}")

            static_repo_dir = self.static_analysis_dir / repo_name

            if not static_repo_dir.exists() or not static_repo_dir.is_dir():
                self.logger.warning(
                    f"Static analysis directory not found for {repo_name}: {static_repo_dir}"
                )
                continue

            architecture_file = self.architecture_dir / f"{repo_name}.json"

            if not architecture_file.exists():
                self.logger.warning(
                    f"Architecture analysis not found for {repo_name}"
                )
                continue

            static_metrics = {}

            for json_file in static_repo_dir.glob("*.json"):
                try:
                    static_metrics[json_file.stem] = json.loads(
                        json_file.read_text(encoding="utf-8")
                    )
                except json.JSONDecodeError as e:
                    self.logger.warning(
                        f"Invalid JSON in {json_file}: {e}"
                    )

            architecture = architecture_file.read_text(encoding="utf-8")
            issues = static_metrics

            tactics_text = "\n".join(
                f"""
ID: {t['AT_ID']}
Name: {t['Tactic_Name']}
Primary QA Impact: {t['Primary_QA_Impact']}
Description: {t['Description']}
Positive Impact: {t['Positive_Impact']}
Negative Impact: {t['Negative_Impact']}
Related Terms: {t['Related_Terms']}
Source: {t['Source']}
""".strip()
                for t in self.tactics
            )

            prompt = f"""
You are a software architecture expert.

ARCHITECTURE:
{architecture}

MAINTAINABILITY ISSUES (static analysis):
{issues}

ARCHITECTURAL TACTICS CATALOG:
{tactics_text}

TASK:
Select the most appropriate architectural tactic to improve maintainability.
Consider trade-offs.

OUTPUT STRICT JSON:
{{
  "selected_tactic": {{
    "id": "...",
    "name": "...",
    "primary_qa_impact": "...",
    "positive_impact": "...",
    "negative_impact": "..."
  }},
  "justification": "...",
  "expected_architectural_change": "...",
  "risks": "..."
}}
"""

            response = self.call_llm(prompt)

            output_file = self.output_dir / f"{repo_name}.json"
            output_file.write_text(response, encoding="utf-8")

            self.logger.info(f"Tactic selected for {repo_name}")

        return repositories


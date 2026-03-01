import csv
import json
from pathlib import Path

from filters.help_methods import safe_llm_json
from pipes_and_filters.pipes_and_filters import Filter
from filters.help_methods import collect_repo_files, build_repo_tree


TACTICS_CATALOG_PATH = Path("architectural_tactics_complete_catalog.csv")


class ArchitectureTacticSelectionFilter(Filter):
    name = "architecture_tactic_selection"

    def __init__(
        self,
        artifacts_dir: Path,
        tactics_catalog: Path,
        model_name: str,
        call_llm
    ):
        super().__init__()
        self.artifacts_dir = artifacts_dir
        self.tactics_catalog = tactics_catalog
        self.tactics = self._load_tactics()
        self.call_llm = call_llm
        self.model_name = model_name

        self.architecture_dir = (
            self.artifacts_dir / f"ai_analysis_{model_name.split(":")[0]}" / "architecture"
        )
        self.static_analysis_dir = (
            self.artifacts_dir / "static_analysis" / "BEFORE"
        )
        self.output_dir = (
            self.artifacts_dir / f"ai_analysis_{model_name.split(":")[0]}" / "architecture_tactics"
        )
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def _load_tactics(self):
        with open(self.tactics_catalog, encoding="utf-8") as f:
            return list(csv.DictReader(f))

    def process(self, repositories: list):
        for repo in repositories:
            try:
                repo_name = repo.name

                if not repo.repo_files:
                    repo.repo_files = collect_repo_files(repo.local_path)
                if not repo.repo_tree:
                    repo.repo_tree = build_repo_tree(repo.local_path)

                output_file = self.output_dir / f"{repo_name}.json"
                if output_file.exists():
                    continue

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
                You are a senior software architect specializing in maintainability improvements of real backend systems.

                ========================================
                WHAT ARE ARCHITECTURAL TACTICS
                ========================================

                Architectural tactics are design decisions applied to the structure of software to improve quality attributes.

                A maintainability tactic typically:

                • reduces code complexity
                • improves modularity
                • improves testability
                • improves separation of concerns
                • improves readability
                • reduces coupling
                • increases cohesion

                Tactics operate on REAL code structure, not theory.

                Examples:

                GOOD tactics:

                - Extract component
                - Introduce abstraction
                - Refactor large module
                - Introduce dependency inversion
                - Separate responsibilities

                BAD tactics:

                - Add comments
                - Rename variables
                - Improve documentation

                These are NOT architectural tactics.

                ========================================
                INPUT DATA
                ========================================

                ARCHITECTURE DESCRIPTION:
                {architecture}

                STATIC ANALYSIS ISSUES:
                {issues}

                REPOSITORY TREE:
                {repo.repo_tree}

                REPOSITORY FILE CONTENTS (signatures only):
                {"".join(
                    f"\n--- FILE: {path} ---\n{content}\n"
                    for path, content in repo.repo_files.items()
                )}

                ========================================
                ARCHITECTURAL TACTICS CATALOG
                ========================================

                You MUST select ONLY ONE tactic from this catalog.

                {tactics_text}

                DO NOT invent new tactics.

                ========================================
                TASK
                ========================================

                Select the SINGLE BEST architectural tactic that:

                • directly addresses REAL maintainability problems in THIS repository
                • can be implemented incrementally
                • can be implemented via code changes
                • fits the actual repository structure

                IMPORTANT:

                You MUST base your decision on:

                • static analysis issues
                • real file structure
                • real modules
                • real architectural problems

                NOT theory.

                ========================================
                SELECTION RULES
                ========================================

                The tactic MUST:

                • improve maintainability

                AND

                • be implementable in this repository

                AND

                • affect identifiable files/modules

                DO NOT select tactics that:

                • require rewriting the entire system
                • require unrealistic changes
                • do not match repository structure

                ========================================
                OUTPUT FORMAT (STRICT JSON ONLY)
                ========================================

                Return ONLY JSON.

                NO markdown.

                NO explanations outside JSON.

                First character MUST be {{


                Required schema:

                {{
                  "selected_tactic": {{
                    "id": "...",
                    "name": "...",
                    "primary_qa_impact": "...",
                    "positive_impact": "...",
                    "negative_impact": "..."
                  }},

                  "justification": "...",

                  "target_components": [
                    "path/to/file.py",
                    "module.name"
                  ],

                  "expected_architectural_change": "...",

                  "implementation_strategy": "...",

                  "risks": "..."
                }}


                ========================================
                JUSTIFICATION REQUIREMENTS
                ========================================

                Justification MUST explain:

                • WHY this tactic
                • WHAT maintainability problem it solves
                • WHERE in repository

                ========================================
                IMPLEMENTATION STRATEGY REQUIREMENTS
                ========================================

                Strategy MUST describe:

                • WHAT to refactor
                • HOW structure will change
                • WHAT new abstractions/modules may appear

                ========================================
                IMPORTANT
                ========================================

                Return ONLY valid JSON.

                Do NOT wrap in ```json

                Do NOT invent tactics.

                Do NOT output multiple tactics.

                Select ONLY ONE.
                """

                response = self.call_llm(prompt=prompt, model=self.model_name)

                data = safe_llm_json(response)

                output_file.write_text(
                    data,
                    encoding="utf-8"
                )

                self.logger.info(f"Tactic selected for {repo_name}")

            except Exception as e:
                self.logger.error(f"Catch Exception: {e} on repo {repo.name}")

        return repositories



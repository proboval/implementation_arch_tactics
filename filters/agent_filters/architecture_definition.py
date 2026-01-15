import json
from pathlib import Path
from pipes_and_filters.pipes_and_filters import Filter


def build_architecture_prompt(
    arch_metrics: dict,
    code_metrics: dict,
):
    return f"""
You are a software architecture expert.

Given the following metrics extracted from a Python project,
determine the most likely software architecture style.

Architecture metrics:
{json.dumps(arch_metrics, indent=2)}

Code maintainability metrics:
{json.dumps(code_metrics, indent=2)}

Choose ONE primary architecture type from:
- layered
- hexagonal (ports and adapters)
- modular_monolith
- script_based
- mvc
- microservices_like
- unclear

Return STRICT JSON with fields:
- architecture_type
- confidence (0.0 - 1.0)
- evidence (list of observations)
- alternatives (list)
- risks (list)

Do not include explanations outside JSON.
"""


class ArchitectureDetectionAgent(Filter):
    name = "architectureDefinition"

    def __init__(self, call_llm, artifacts_dir: Path):
        super().__init__()
        self.call_llm = call_llm

        self.static_dir = (
            artifacts_dir / "static_analysis" / "BEFORE"
        )
        self.out_dir = (
            artifacts_dir / "ai_analysis" / "architecture"
        )
        self.out_dir.mkdir(parents=True, exist_ok=True)

    def process(self, repositories: list):
        """
        repositories: list of repo objects (with .name)
        """

        for repo in repositories:
            repo_dir = self.static_dir / repo.name

            arch_file = repo_dir / "architecture_maintainability.json"
            code_file = repo_dir / "code_maintainability.json"

            if not arch_file.exists() or not code_file.exists():
                continue

            arch_metrics = json.loads(arch_file.read_text())
            code_metrics = json.loads(code_file.read_text())

            prompt = build_architecture_prompt(
                arch_metrics, code_metrics
            )

            response = self.call_llm(prompt)

            data = json.loads(response)

            out_file = self.out_dir / f"{repo.name}.json"
            out_file.write_text(
                json.dumps(data, indent=2)
            )

        return repositories


import json
from pathlib import Path
from pipes_and_filters.pipes_and_filters import Filter
from filters.help_methods import build_repo_tree, collect_repo_files, safe_llm_json


def build_architecture_prompt(
    arch_metrics: dict,
    code_metrics: dict,
    repo_files,
    repo_tree
):
    return f"""
You are a software architecture expert.

Given the following metrics extracted from a Python project,
determine the most likely software architecture style.

Architecture metrics:
{json.dumps(arch_metrics, indent=2)}

Code maintainability metrics:
{json.dumps(code_metrics, indent=2)}

Repository tree:
{repo_tree}

Repository files content:
{"".join(
    f"\n--- FILE: {path} ---\n{content}\n"
    for path, content in repo_files.items()
)}

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

IMPORTANT:
- Return ONLY raw JSON
- Do NOT use markdown
- Do NOT wrap in ```json
- The first character of the response MUST be {{ or [
"""


class ArchitectureDetectionAgent(Filter):
    name = "architectureDefinition"

    def __init__(self, call_llm, artifacts_dir: Path, model_name: str):
        super().__init__()
        self.call_llm = call_llm
        self.model_name = model_name

        self.static_dir = (
            artifacts_dir / "static_analysis" / "BEFORE"
        )
        self.out_dir = (
            artifacts_dir / f"ai_analysis_{model_name.split(":")[0]}" / "architecture"
        )
        self.out_dir.mkdir(parents=True, exist_ok=True)

        self.context = []

    def process(self, repositories: list):
        """
        repositories: list of repo objects (with .name)
        """

        for repo in repositories:
            try:
                repo_dir = self.static_dir / repo.name

                out_file = self.out_dir / f"{repo.name}.json"

                if out_file.exists():
                    continue

                arch_file = repo_dir / "architecture_maintainability.json"
                code_file = repo_dir / "code_maintainability.json"

                if not arch_file.exists() or not code_file.exists():
                    continue

                arch_metrics = json.loads(arch_file.read_text())
                code_metrics = json.loads(code_file.read_text())

                repo.repo_tree = build_repo_tree(repo.local_path)
                repo.repo_files = collect_repo_files(repo.local_path, signatures_only=True)

                prompt = build_architecture_prompt(
                    arch_metrics, code_metrics, repo.repo_files, repo.repo_tree
                )

                response = self.call_llm(prompt=prompt, model=self.model_name)

                data = safe_llm_json(response)

                self.logger.info(f"Architecture detect for {repo.name}")

                out_file.write_text(
                    data,
                    encoding="utf-8"
                )
            except Exception as e:
                self.logger.error(f"Catch Exception: {e} on repo {repo.name}")

        return repositories


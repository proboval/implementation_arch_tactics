from pathlib import Path

from filters.agent_filters.architecture_definition import ArchitectureDetectionAgent
from filters.agent_filters.call_llm import call_llm
from filters.github_search import GitHubSearchFilter
from filters.github_clone import CloneRepositoriesFilter
from filters.static_analysis.before import StaticAnalysisFilter
from filters.agent_filters.tactic_definition import ArchitectureTacticSelectionFilter
from filters.agent_filters.tactic_implementation import ArchitecturalTacticImplementationAgent
from pipes_and_filters.pipes_and_filters import Pipeline
from dotenv import load_dotenv
import os


load_dotenv()

GITHUB_TOKEN = os.getenv("GIT_KEY")

pipeline = Pipeline(
    filters=[
        GitHubSearchFilter(token=GITHUB_TOKEN, max_repos=2),

        # CloneRepositoriesFilter(
        #     base_dir=Path("./artifacts/repos"),
        #     output_file=Path("./artifacts/cloned_repositories.txt"),
        # ),
        #
        # StaticAnalysisFilter(
        #     artifacts_dir=Path("./artifacts"),
        #     step="BEFORE"
        # ),
        #
        # ArchitectureDetectionAgent(
        #     call_llm=call_llm,
        #     artifacts_dir=Path("./artifacts"),
        # ),
        #
        # ArchitectureTacticSelectionFilter(
        #     artifacts_dir=Path("./artifacts"),
        #     tactics_catalog=Path(
        #         "./filters/agent_filters/architectural_tactics_complete_catalog.csv"
        #     ),
        #     call_llm=call_llm
        # ),

        ArchitecturalTacticImplementationAgent(
            call_llm=call_llm,
            artifacts_dir=Path("./artifacts"),
        ),

        StaticAnalysisFilter(
            artifacts_dir=Path("./artifacts"),
            step="AFTER"
        ),
    ]
)

repositories = pipeline.run(None)

for repo in repositories:
    print(repo.full_name, repo.stars, repo.size_kb)

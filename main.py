from pathlib import Path

from filters.agent_filters.architecture_definition import ArchitectureDetectionAgent
from filters.agent_filters.call_llm import call_llm
from filters.github_filters.github_search import GitHubSearchFilter
from filters.github_filters.github_clone import CloneRepositoriesFilter
from filters.static_analysis.before import StaticAnalysisFilter
from filters.agent_filters.tactic_definition import ArchitectureTacticSelectionFilter
from filters.agent_filters.tactic_implementation import ArchitecturalTacticImplementationAgent
from filters.dataset_filters.datase_create import BackendDatasetPreparationFilter
from pipes_and_filters.pipes_and_filters import Pipeline
from dotenv import load_dotenv
import os


load_dotenv()

GITHUB_TOKEN = os.getenv("GIT_KEY")
MODEL_NAME = "qwen3-coder:480b-cloud"
ARTIFACTS_DIR_NAME = "artifacts_create_dataset"

pipeline = Pipeline(
    filters=[
        GitHubSearchFilter(
            token=GITHUB_TOKEN,
            max_repos=5,
            output_file=Path(f"./{ARTIFACTS_DIR_NAME}/cloned_repositories.txt")
        ),

        BackendDatasetPreparationFilter(
            workdir=Path(f"./{ARTIFACTS_DIR_NAME}"),
            output_csv=Path(f"./{ARTIFACTS_DIR_NAME}/dataset")
        ),

        # CloneRepositoriesFilter(
        #     base_dir=Path(f"./{ARTIFACTS_DIR_NAME}/repos"),
        # ),
        #
        # StaticAnalysisFilter(
        #     artifacts_dir=Path(f"./{ARTIFACTS_DIR_NAME}"),
        #     step="BEFORE"
        # ),
        #
        # ArchitectureDetectionAgent(
        #     call_llm=call_llm,
        #     artifacts_dir=Path(f"./{ARTIFACTS_DIR_NAME}"),
        #     model_name=MODEL_NAME
        # ),
        #
        # ArchitectureTacticSelectionFilter(
        #     artifacts_dir=Path(f"./{ARTIFACTS_DIR_NAME}"),
        #     tactics_catalog=Path(
        #         "./filters/agent_filters/architectural_tactics_complete_catalog.csv"
        #     ),
        #     call_llm=call_llm,
        #     model_name=MODEL_NAME
        # ),
        #
        # ArchitecturalTacticImplementationAgent(
        #     call_llm=call_llm,
        #     model_name=MODEL_NAME,
        #     artifacts_dir=Path(f"./{ARTIFACTS_DIR_NAME}"),
        #     max_iterations=10,
        # ),
        #
        # StaticAnalysisFilter(
        #     artifacts_dir=Path(f"./{ARTIFACTS_DIR_NAME}"),
        #     step="AFTER"
        # ),
    ]
)

pipeline.run()

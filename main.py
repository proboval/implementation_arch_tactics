from pathlib import Path

from filters.agent_filters.architecture_definition import ArchitectureDetectionAgent
from filters.agent_filters.call_llm import call_llm
from filters.github_filters.github_search import GitHubSearchFilter
from filters.dataset_filters.collect_github_stars import DatasetMergeAndEnrichFilter
from filters.github_filters.github_clone import CloneRepositoriesFilter
from filters.static_analysis.before import StaticAnalysisFilter
from filters.agent_filters.tactic_definition import ArchitectureTacticSelectionFilter
from filters.agent_filters.tactic_implementation import ArchitecturalTacticImplementationAgent
from filters.dataset_filters.dataset_create import BackendDatasetPreparationFilter
from filters.dataset_filters.maintainability_calc import DatasetMaintainabilityEnricher
from pipes_and_filters.pipes_and_filters import Pipeline
from dotenv import load_dotenv
from filters.config import GITHUB_TOKEN,ARTIFACTS_DIR_NAME,MODEL_NAME,STARS
from filters.agent_filters.maintainability_improvement_filter import DatasetLLMImprovementRunner


static_filter = StaticAnalysisFilter(
    artifacts_dir=Path(f"./{ARTIFACTS_DIR_NAME}/artifacts"),
    step="BEFORE",
)

architecture_filter = ArchitectureDetectionAgent(
            call_llm=call_llm,
            artifacts_dir=Path(f"./{ARTIFACTS_DIR_NAME}/artifacts"),
            model_name=MODEL_NAME
        )

tactic_filter = ArchitectureTacticSelectionFilter(
            artifacts_dir=Path(f"./{ARTIFACTS_DIR_NAME}/artifacts"),
            tactics_catalog=Path(
                "./filters/agent_filters/architectural_tactics_complete_catalog.csv"
            ),
            call_llm=call_llm,
            model_name=MODEL_NAME
        )

implementation_filter = ArchitecturalTacticImplementationAgent(
            call_llm=call_llm,
            model_name=MODEL_NAME,
            artifacts_dir=Path(f"./{ARTIFACTS_DIR_NAME}/artifacts"),
            max_iterations=100,
            repo_path=Path(f"./{ARTIFACTS_DIR_NAME}/repos")
        )

def maintainability_filter_factory(step: str):
    return StaticAnalysisFilter(
        artifacts_dir=Path("artifacts"),
        step=step,
    )

pipeline = Pipeline(
    filters=[
        DatasetLLMImprovementRunner(
            input_csv=Path(f"./{ARTIFACTS_DIR_NAME}/maintainability_dataset.csv"),
            output_csv=Path(f"./{ARTIFACTS_DIR_NAME}/improvement_maintainability_dataset.csv"),
            workdir=Path(f"./{ARTIFACTS_DIR_NAME}/repos"),
            architecture_filter=architecture_filter,
            tactic_filter=tactic_filter,
            implementation_filter=implementation_filter,
            maintainability_filter_factory=maintainability_filter_factory
        ),
        # DatasetMaintainabilityEnricher(
        #     dataset_csv=Path(f"./{ARTIFACTS_DIR_NAME}/stars_dataset.csv"),
        #     output_csv=Path(f"./{ARTIFACTS_DIR_NAME}/maintainability_dataset.csv"),
        #     artifacts_dir=Path(f"./{ARTIFACTS_DIR_NAME}/artifacts"),
        #     static_analysis_filter=static_filter,
        #     workdir=Path(f"./{ARTIFACTS_DIR_NAME}/repos"),
        # ),
        # DatasetMergeAndEnrichFilter(
        #     input_dir=Path(f"./{ARTIFACTS_DIR_NAME}"),
        #     output_csv=Path(f"./{ARTIFACTS_DIR_NAME}/stars_dataset.csv"),
        #     github_token=GITHUB_TOKEN,
        # ),
        # GitHubSearchFilter(
        #     token=GITHUB_TOKEN,
        #     max_repos=300,
        #     output_file=Path(f"./{ARTIFACTS_DIR_NAME}/cloned_repositories.txt"),
        #     stars=STARS
        # ),
        #
        # BackendDatasetPreparationFilter(
        #     workdir=Path(f"./{ARTIFACTS_DIR_NAME}/repos"),
        #     output_csv=Path(f"./{ARTIFACTS_DIR_NAME}/dataset_{STARS[0]}_{STARS[1]}.csv")
        # ),

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

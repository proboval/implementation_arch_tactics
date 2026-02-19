from filters.help_methods import add_maintainability_to_csv
from pathlib import Path


add_maintainability_to_csv(
    artifacts_dir=Path("./artifacts_experiment_2/artifacts"),
    csv_file=Path("experiments/results/improvement_maintainability_experiment_2.csv"),
)

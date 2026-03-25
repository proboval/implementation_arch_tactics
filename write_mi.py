from filters.help_methods import add_maintainability_to_csv, del_extra_dir
from pathlib import Path


add_maintainability_to_csv(
    artifacts_dir=Path("experiment_4_new_repos/artifacts"),
    csv_file=Path("experiments/improvement_maintainability_experiment_4.csv"),
)

# del_extra_dir(
#     artifacts_dir=Path("./artifacts_experiment_3/artifacts/static_analysis/AFTER"),
#     csv_file=Path("./artifacts_experiment_3/dataset.csv"),
# )

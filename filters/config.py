import os
from dotenv import load_dotenv


load_dotenv()

GITHUB_TOKEN = os.getenv("GIT_KEY")
MODEL_NAME = "qwen3-coder-next:cloud"
ARTIFACTS_DIR_NAME = "artifacts_experiment_3"
STARS = (1, 20)

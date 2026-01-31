import os
from dotenv import load_dotenv


load_dotenv()


GITHUB_TOKEN = os.getenv("GIT_KEY")
MODEL_NAME = "qwen3-coder:480b-cloud"
ARTIFACTS_DIR_NAME = "artifacts_create_dataset"
STARS = (1, 20)

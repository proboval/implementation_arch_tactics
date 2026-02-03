import os
from dotenv import load_dotenv


load_dotenv()


GITHUB_TOKEN = os.getenv("GIT_KEY")
MODEL_NAME = "gemma3:latest"
ARTIFACTS_DIR_NAME = "artifacts_create_dataset"
STARS = (1, 20)

import csv
import shutil
import subprocess
import time
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

from pipes_and_filters.pipes_and_filters import Filter, Repository


# =========================
# CONFIG
# =========================

ML_KEYWORDS = {
    "torch",
    "tensorflow",
    "sklearn",
    "scikit-learn",
    "keras",
    "xgboost",
    "lightgbm",
    "catboost",
    "transformers",
    "langchain",
    "openai",
}

EXCLUDED_DIRS = {
    "notebooks",
    "experiments",
    "examples",
    "ml",
    "ai",
    "docs",
}


# =========================
# DETECTION MODELS
# =========================

@dataclass
class ArchitectureDetectionResult:
    name: str
    score: int
    confidence: float


class ArchitectureDetector:

    name: str = "base"

    def detect(self, repo_path: Path) -> Optional[ArchitectureDetectionResult]:
        raise NotImplementedError


# =========================
# DJANGO DETECTOR
# =========================

class DjangoDetector(ArchitectureDetector):

    name = "django_mvc"

    def detect(self, repo_path: Path):

        score = 0

        req = repo_path / "requirements.txt"

        if req.exists():

            text = req.read_text(
                encoding="utf-8",
                errors="ignore"
            ).lower()

            if "django" in text:
                score += 4

        if (repo_path / "manage.py").exists():
            score += 3

        if list(repo_path.rglob("settings.py")):
            score += 2

        if list(repo_path.rglob("models.py")):
            score += 2

        if list(repo_path.rglob("views.py")):
            score += 2

        if list(repo_path.rglob("templates")):
            score += 1

        if score < 7:
            return None

        return ArchitectureDetectionResult(
            name=self.name,
            score=score,
            confidence=min(score / 12, 1.0)
        )


# =========================
# FLASK DETECTOR
# =========================

class FlaskDetector(ArchitectureDetector):

    name = "flask_mvc"

    def detect(self, repo_path: Path):

        score = 0

        req = repo_path / "requirements.txt"

        if req.exists():

            text = req.read_text(
                encoding="utf-8",
                errors="ignore"
            ).lower()

            if "flask" in text:
                score += 4

        if list(repo_path.rglob("app.py")):
            score += 2

        if list(repo_path.rglob("wsgi.py")):
            score += 2

        if list(repo_path.rglob("templates")):
            score += 2

        for file in repo_path.rglob("*.py"):

            try:

                text = file.read_text(errors="ignore")

                if "@app.route" in text:
                    score += 2
                    break

            except:
                pass

        if score < 6:
            return None

        return ArchitectureDetectionResult(
            name=self.name,
            score=score,
            confidence=min(score / 10, 1.0)
        )


# =========================
# FASTAPI DETECTOR
# =========================

class FastAPIDetector(ArchitectureDetector):

    name = "fastapi"

    def detect(self, repo_path: Path):

        score = 0

        req = repo_path / "requirements.txt"

        if req.exists():

            text = req.read_text(
                encoding="utf-8",
                errors="ignore"
            ).lower()

            if "fastapi" in text:
                score += 4

        for file in repo_path.rglob("*.py"):

            try:

                text = file.read_text(errors="ignore")

                if "FastAPI(" in text:
                    score += 3

                if "@app.get" in text or "@router.get" in text:
                    score += 2

            except:
                pass

        if score < 6:
            return None

        return ArchitectureDetectionResult(
            name=self.name,
            score=score,
            confidence=min(score / 10, 1.0)
        )


# =========================
# DATASET PIPELINE CORE
# =========================

class ArchitecturePipeline:

    def __init__(self):

        self.detectors = [
            DjangoDetector(),
            FlaskDetector(),
            FastAPIDetector(),
        ]

    def detect(self, repo_path: Path):

        results = []

        for detector in self.detectors:

            result = detector.detect(repo_path)

            if result:
                results.append(result)

        if not results:
            return None

        return max(results, key=lambda r: r.score)


# =========================
# MAIN FILTER
# =========================

class BackendDatasetPreparationFilter(Filter):

    name = "backend_dataset_preparation"

    def __init__(
        self,
        workdir: Path,
        output_csv: Path,
        max_repos: Optional[int] = None,
    ):

        super().__init__()

        self.workdir = workdir
        self.output_csv = output_csv
        self.max_repos = max_repos

        self.pipeline = ArchitecturePipeline()

        self.workdir.mkdir(parents=True, exist_ok=True)


    # =========================
    # MAIN PROCESS
    # =========================

    def process(self, repositories: List[Repository]):

        dataset_rows = []

        for idx, repo in enumerate(repositories):

            if self.max_repos and idx >= self.max_repos:
                break

            try:

                row = self.process_repo(repo)

                if row:
                    dataset_rows.append(row)

            except Exception as e:

                self.logger.error(
                    f"Failed {repo.full_name}: {e}"
                )

        self.write_csv(dataset_rows)

        return repositories


    # =========================
    # PROCESS SINGLE REPO
    # =========================

    def process_repo(self, repo: Repository):

        repo_path = self.workdir / repo.name

        self.clone_repo(repo.url, repo_path)

        try:

            if not self.is_backend_repo(repo_path):
                self.logger.info(f"[SKIP] {repo.full_name}")
                return None

            arch = self.pipeline.detect(repo_path)

            if not arch:
                self.logger.info(f"[NO ARCH] {repo.full_name}")
                return None

            self.logger.info(
                f"[OK] {repo.full_name} | {arch.name} | score={arch.score}"
            )
            return {
                "full_name": repo.full_name,
                "clone_url": repo.url,
                "architecture": arch.name,
                "score": arch.score,
                "confidence": arch.confidence,
            }
        finally:
            time.sleep(1)
            shutil.rmtree(repo_path, ignore_errors=True)


    # =========================
    # BACKEND FILTER
    # =========================

    def is_backend_repo(self, repo_path: Path):

        req = repo_path / "requirements.txt"

        if not req.exists():
            return False

        text = req.read_text(
            encoding="utf-8",
            errors="ignore"
        ).lower()

        if any(kw in text for kw in ML_KEYWORDS):
            return False


        py_files = list(repo_path.rglob("*.py"))

        if not py_files:
            return False


        for file in py_files:

            if any(
                part.lower() in EXCLUDED_DIRS
                for part in file.parts
            ):
                return False

        return True

    # =========================
    # GIT
    # =========================

    def clone_repo(self, url: str, path: Path):
        subprocess.run(
            ["git", "clone", "--depth", "1", url, str(path)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

    # =========================
    # CSV
    # =========================

    def write_csv(self, rows: List[dict]):
        self.output_csv.parent.mkdir(
            parents=True,
            exist_ok=True
        )
        with self.output_csv.open(
            "w",
            newline="",
            encoding="utf-8"
        ) as f:
            writer = csv.DictWriter(
                f,
                fieldnames=[
                    "full_name",
                    "clone_url",
                    "architecture",
                    "score",
                    "confidence",
                ],
            )

            writer.writeheader()
            writer.writerows(rows)

        self.logger.info(
            f"Saved {len(rows)} repositories"
        )
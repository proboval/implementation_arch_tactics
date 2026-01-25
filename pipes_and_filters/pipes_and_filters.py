from abc import ABC, abstractmethod
from typing import Iterable, List
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Dict, Any
from filters.logger import get_filter_logger
import time


@dataclass
class Repository:
    name: str
    full_name: str
    url: str
    stars: int
    forks: int
    size_kb: int
    language: str

    local_path: Optional[Path] = None

    metadata: Dict[str, Any] = None
    static_analysis_before: Dict[str, Any] = None
    static_analysis_after: Dict[str, Any] = None

    architecture: Optional[str] = None
    analysis_strategy: Optional[str] = None
    changes_metrics: Dict[str, Any] = None

    repo_files: dict[str, str] = None
    repo_tree: str = None


class Filter(ABC):
    name = "base"

    def __init__(self):
        self.logger = get_filter_logger(self.name)

    def run(self, data):
        start = time.time()
        self.logger.info(f"{self.name} |START")

        try:
            result = self.process(data)
            duration = round(time.time() - start, 2)

            self.logger.info(f"{self.name} | SUCCESS | time={duration}s")
            return result

        except Exception as e:
            duration = round(time.time() - start, 2)
            self.logger.error(f"{self.name} | FAILED | time={duration}s | error={e}")

    @abstractmethod
    def process(self, data: Iterable[Repository]) -> List[Repository]:
        pass


class Pipeline:
    def __init__(self, filters: list[Filter]):
        self.filters = filters

    def run(self, data=None):
        for f in self.filters:
            data = f.run(data)
        return data

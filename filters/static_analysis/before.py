import subprocess
import json
import os
import ast
from pathlib import Path
from typing import Iterable, List, Dict
from pipes_and_filters.pipes_and_filters import Filter, Repository
import re


ANSI_ESCAPE_RE = re.compile(r"\x1B\[[0-?]*[ -/]*[@-~]")

def strip_ansi(text: str) -> str:
    return ANSI_ESCAPE_RE.sub("", text)


class StaticAnalysisFilter(Filter):
    name = "StaticAnalysis"

    def __init__(self, artifacts_dir: Path, step):
        super().__init__()
        self.artifacts_dir = artifacts_dir
        self.before_dir = artifacts_dir / "static_analysis" / step
        self.before_dir.mkdir(parents=True, exist_ok=True)
        self.name = f"StaticAnalysis{step}"

    def process(self, data: Iterable[Repository]) -> List[Repository]:
        for repo in data:
            if not repo.local_path:
                continue

            repo_dir = self.before_dir / repo.name

            if repo_dir.exists():
                self.logger.info(f"{repo_dir} exists")
                continue

            repo_dir.mkdir(parents=True, exist_ok=True)

            maintainability = self._run_radon(repo.local_path, repo_dir)
            architecture = self._analyze_architecture(repo.local_path, repo_dir)

            self._compute_code_maintainability(maintainability, repo_dir)
            self._compute_architecture_maintainability(architecture, repo_dir)
            self._compute_documentation_maintainability(repo, repo_dir)

        return list(data)

    # ---------- MAINTAINABILITY ----------
    def _run_radon(self, repo_path: Path, out_dir: Path) -> Dict:
        out_file = out_dir / "radon_mi.json"

        try:
            result = subprocess.run(
                ["radon", "mi", "--json", str(repo_path)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=False,
            )

            clean_stdout = strip_ansi(result.stdout)
            data = json.loads(clean_stdout)

        except Exception as e:
            data = {"error": str(e)}

        out_file.write_text(
            json.dumps(data, indent=2), encoding="utf-8"
        )
        return data

    # ---------- ARCHITECTURE PROXIES ----------
    def _analyze_architecture(self, repo_path: Path, out_dir: Path) -> Dict:
        out_file = out_dir / "architecture_proxies.json"

        py_files = list(repo_path.rglob("*.py"))

        package_dirs = set()
        max_depth = 0
        imports = {}

        for file in py_files:
            try:
                rel_path = file.relative_to(repo_path)
                depth = len(rel_path.parents)
                max_depth = max(max_depth, depth)

                if file.name == "__init__.py":
                    package_dirs.add(file.parent)

                tree = ast.parse(file.read_text())
                file_imports = set()

                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for n in node.names:
                            file_imports.add(n.name.split(".")[0])
                    elif isinstance(node, ast.ImportFrom):
                        if node.module:
                            file_imports.add(node.module.split(".")[0])

                imports[str(rel_path)] = list(file_imports)

            except Exception:
                continue

        data = {
            "python_files": len(py_files),
            "packages": len(package_dirs),
            "max_directory_depth": max_depth,
            "avg_files_per_package": (
                len(py_files) / len(package_dirs)
                if package_dirs else 0
            ),
            "imports_graph": imports,
        }

        out_file.write_text(
            json.dumps(data, indent=2), encoding="utf-8"
        )
        return data

    def _compute_code_maintainability(self, radon_data: Dict, repo_dir: Path):
        out = repo_dir / "code_maintainability.json"

        mis = [
            v["mi"]
            for v in radon_data.values()
            if isinstance(v, dict) and "mi" in v
        ]

        data = {
            "mi_avg": sum(mis) / len(mis) if mis else 0,
            "mi_min": min(mis) if mis else 0,
            "files_analyzed": len(mis),
            "factors": ["T4", "A1"],
        }

        out.write_text(json.dumps(data, indent=2))

    def _compute_architecture_maintainability(self, arch: Dict, repo_dir: Path):
        out = repo_dir / "architecture_maintainability.json"

        imports = arch.get("imports_graph", {})
        fan_out = [len(v) for v in imports.values()]

        data = {
            "packages": arch.get("packages", 0),
            "avg_fan_out": sum(fan_out) / len(fan_out) if fan_out else 0,
            "max_directory_depth": arch.get("max_directory_depth", 0),
            "factors": ["C1", "C2", "A3"],
        }

        out.write_text(json.dumps(data, indent=2))

    def _compute_documentation_maintainability(self, repo, repo_dir: Path):
        out = repo_dir / "documentation_maintainability.json"

        py_files = list(repo.local_path.rglob("*.py"))
        with_docstring = 0

        for f in py_files:
            try:
                tree = ast.parse(f.read_text())
                if ast.get_docstring(tree):
                    with_docstring += 1
            except Exception:
                continue

        readme = any(
            f.name.lower().startswith("readme")
            for f in repo.local_path.iterdir()
        )

        data = {
            "has_readme": readme,
            "docstring_coverage": (
                with_docstring / len(py_files) if py_files else 0
            ),
            "factors": ["U2", "U3", "T5", "A2"],
        }

        out.write_text(json.dumps(data, indent=2))


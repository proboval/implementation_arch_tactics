import ast
import base64
import csv
import json
import os
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Dict, List, Set, Tuple
from dotenv import load_dotenv


load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
INPUT_CSV = "dataset_normalized.csv"   # или dataset.csv
OUTPUT_DIR = Path("artifacts/repo_artifacts")

MAX_TREE_DEPTH = 6
MAX_SIGNATURE_FILE_SIZE = 15_000
MAX_SIGNATURE_FILES = 200

EXCLUDED_DIRS = {
    ".git",
    "__pycache__",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".tox",
    ".venv",
    "venv",
    "env",
    "node_modules",
    ".idea",
    ".vscode",
    "dist",
    "build",
    ".eggs",
}


def build_repo_tree(root: Path, max_depth: int = 6) -> str:
    """
    Build ASCII tree of repository structure.
    """
    lines = []

    def walk(dir_path: Path, prefix: str = "", depth: int = 0):
        if depth > max_depth:
            return

        try:
            entries = sorted(
                [p for p in dir_path.iterdir() if p.name not in EXCLUDED_DIRS],
                key=lambda p: (p.is_file(), p.name.lower()),
            )
        except PermissionError:
            lines.append(f"{prefix}└── [permission denied]")
            return

        for idx, path in enumerate(entries):
            connector = "└── " if idx == len(entries) - 1 else "├── "
            lines.append(f"{prefix}{connector}{path.name}")

            if path.is_dir():
                extension = "    " if idx == len(entries) - 1 else "│   "
                walk(path, prefix + extension, depth + 1)

    lines.append(root.name)
    walk(root)

    return "\n".join(lines)


def extract_python_signatures(source: str) -> str:
    """
    Extract imports, class signatures and function signatures from Python code.
    """
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return ""

    lines = []

    for node in tree.body:
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            segment = ast.get_source_segment(source, node)
            if segment:
                lines.append(segment)

        elif isinstance(node, ast.ClassDef):
            bases = [
                ast.get_source_segment(source, b) or "?"
                for b in node.bases
            ]
            base_str = f"({', '.join(bases)})" if bases else ""
            lines.append(f"\nclass {node.name}{base_str}:")

            for item in node.body:
                if isinstance(item, ast.FunctionDef):
                    args = ast.get_source_segment(source, item.args)
                    lines.append(f"    def {item.name}{args}: ...")
                elif isinstance(item, ast.AsyncFunctionDef):
                    args = ast.get_source_segment(source, item.args)
                    lines.append(f"    async def {item.name}{args}: ...")

        elif isinstance(node, ast.FunctionDef):
            args = ast.get_source_segment(source, node.args)
            lines.append(f"\ndef {node.name}{args}: ...")

        elif isinstance(node, ast.AsyncFunctionDef):
            args = ast.get_source_segment(source, node.args)
            lines.append(f"\nasync def {node.name}{args}: ...")

    return "\n".join(lines).strip()


def collect_repo_files(
    root: Path,
    max_file_size: int = 15_000,
    max_files: int = 200,
    signatures_only: bool = False,
) -> Dict[str, str]:
    """
    Collect file contents for LLM context.

    If signatures_only=True:
    - Python files are reduced to imports + class/function signatures
    """
    files: Dict[str, str] = {}
    count = 0

    for path in root.rglob("*"):
        if count >= max_files:
            break

        if path.is_dir():
            continue

        if any(part in EXCLUDED_DIRS for part in path.parts):
            continue

        if path.suffix.lower() not in {".py"}:
            continue

        try:
            content = path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue

        if path.suffix == ".py" and signatures_only:
            content = extract_python_signatures(content)

        if not content.strip():
            continue

        if len(content) > max_file_size:
            content = (
                content[:max_file_size]
                + "\n\n# --- TRUNCATED: file too large ---\n"
            )

        rel_path = path.relative_to(root).as_posix()
        files[rel_path] = content
        count += 1

    return files


def format_repo_files(files: Dict[str, str]) -> str:
    """
    Format collected files into one text blob.
    """
    parts = []
    for rel_path in sorted(files.keys()):
        parts.append(f"# FILE: {rel_path}\n")
        parts.append(files[rel_path].rstrip())
        parts.append("\n\n")
    return "".join(parts).strip() + "\n"


def iter_python_files(root: Path):
    for path in root.rglob("*.py"):
        if path.is_dir():
            continue
        if any(part in EXCLUDED_DIRS for part in path.parts):
            continue
        yield path


def module_info_from_path(root: Path, path: Path) -> Tuple[str, str]:
    """
    Returns:
    - module_name
    - current_package
    """
    rel = path.relative_to(root)
    parts = list(rel.parts)

    if parts[-1] == "__init__.py":
        package_parts = parts[:-1]
        module_name = ".".join(package_parts)
        current_package = module_name
    else:
        stem = path.stem
        package_parts = parts[:-1]
        module_name = ".".join(package_parts + [stem])
        current_package = ".".join(package_parts)

    return module_name, current_package


def resolve_relative_module(current_package: str, level: int, module: str | None) -> str:
    """
    Resolve relative import to absolute-ish module path within repository context.

    Examples:
    current_package='app.services', level=1, module='utils' -> 'app.services.utils'
    current_package='app.services', level=2, module='db' -> 'app.db'
    """
    pkg_parts = current_package.split(".") if current_package else []

    # from .x import y  => level=1 means current package
    # from ..x import y => level=2 means parent package
    cut = max(len(pkg_parts) - (level - 1), 0)
    base_parts = pkg_parts[:cut]

    if module:
        module_parts = module.split(".")
        full = base_parts + module_parts
    else:
        full = base_parts

    return ".".join([p for p in full if p])


def collect_internal_modules(root: Path) -> Tuple[Set[str], Dict[str, str], Dict[str, str]]:
    """
    Returns:
    - internal_modules: set of module names
    - path_to_module: rel_path -> module_name
    - path_to_package: rel_path -> current_package
    """
    internal_modules: Set[str] = set()
    path_to_module: Dict[str, str] = {}
    path_to_package: Dict[str, str] = {}

    for path in iter_python_files(root):
        rel_path = path.relative_to(root).as_posix()
        module_name, current_package = module_info_from_path(root, path)

        path_to_module[rel_path] = module_name
        path_to_package[rel_path] = current_package

        if module_name:
            internal_modules.add(module_name)

    return internal_modules, path_to_module, path_to_package


def build_import_graph(root: Path) -> Tuple[List[str], List[Tuple[str, str]]]:
    """
    Build internal import graph between Python modules inside the repository.

    Returns:
    - sorted list of nodes
    - sorted list of edges (source, target)
    """
    internal_modules, path_to_module, path_to_package = collect_internal_modules(root)
    edges: Set[Tuple[str, str]] = set()
    nodes: Set[str] = set(internal_modules)

    for path in iter_python_files(root):
        rel_path = path.relative_to(root).as_posix()
        source_module = path_to_module.get(rel_path, "")
        current_package = path_to_package.get(rel_path, "")

        if not source_module:
            continue

        try:
            source = path.read_text(encoding="utf-8", errors="ignore")
            tree = ast.parse(source)
        except Exception:
            continue

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    target = alias.name
                    if target in internal_modules:
                        edges.add((source_module, target))
                    else:
                        # если импортируется пакет, а не конкретный модуль
                        prefix_matches = [m for m in internal_modules if m.startswith(target + ".")]
                        if prefix_matches:
                            edges.add((source_module, target))

            elif isinstance(node, ast.ImportFrom):
                # resolve base module
                if node.level and node.level > 0:
                    base_module = resolve_relative_module(
                        current_package=current_package,
                        level=node.level,
                        module=node.module,
                    )
                else:
                    base_module = node.module or ""

                if not base_module and node.names:
                    # from . import x
                    for alias in node.names:
                        if alias.name == "*":
                            continue
                        target = resolve_relative_module(
                            current_package=current_package,
                            level=max(node.level, 1),
                            module=alias.name,
                        )
                        if target in internal_modules:
                            edges.add((source_module, target))
                    continue

                # сначала пробуем более точный target: base.alias
                added_specific = False
                for alias in node.names:
                    if alias.name == "*":
                        continue

                    specific_target = f"{base_module}.{alias.name}" if base_module else alias.name
                    if specific_target in internal_modules:
                        edges.add((source_module, specific_target))
                        added_specific = True

                # если точные подмодули не найдены — добавляем base_module
                if not added_specific and base_module:
                    if base_module in internal_modules:
                        edges.add((source_module, base_module))
                    else:
                        prefix_matches = [m for m in internal_modules if m.startswith(base_module + ".")]
                        if prefix_matches:
                            edges.add((source_module, base_module))

    node_list = sorted(nodes)
    edge_list = sorted(edges)
    return node_list, edge_list


def format_import_graph_text(nodes: List[str], edges: List[Tuple[str, str]]) -> str:
    lines = []
    lines.append(f"# Nodes: {len(nodes)}")
    lines.append(f"# Edges: {len(edges)}")
    lines.append("")

    for src, dst in edges:
        lines.append(f"{src} -> {dst}")

    return "\n".join(lines).strip() + "\n"


def clone_repo(repo_full_name: str, target_dir: Path) -> bool:
    repo_url = f"https://github.com/{repo_full_name}.git"

    cmd = ["git"]

    if GITHUB_TOKEN:
        # GitHub принимает Basic auth, где логин можно задать как x-access-token
        auth_value = base64.b64encode(
            f"x-access-token:{GITHUB_TOKEN}".encode("utf-8")
        ).decode("utf-8")

        cmd += [
            "-c",
            f"http.extraheader=AUTHORIZATION: basic {auth_value}",
        ]

    cmd += [
        "clone",
        "--depth",
        "1",
        repo_url,
        str(target_dir),
    ]

    try:
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
        )
        if result.returncode != 0:
            print(f"[CLONE ERROR] {repo_full_name}")
            print(result.stderr.strip())
            return False
        return True
    except Exception as e:
        print(f"[CLONE EXCEPTION] {repo_full_name}: {e}")
        return False


def process_repo(repo_full_name: str):
    repo_full_name = repo_full_name.strip()
    if "/" not in repo_full_name:
        print(f"[SKIP] invalid repo name: {repo_full_name}")
        return

    owner, repo = repo_full_name.split("/", 1)

    output_repo_dir = OUTPUT_DIR / owner / repo
    output_repo_dir.mkdir(parents=True, exist_ok=True)

    repo_tree_file = output_repo_dir / "repo_tree.txt"
    import_graph_file = output_repo_dir / "import_graph.txt"
    import_graph_json_file = output_repo_dir / "import_graph.json"
    repo_signatures_file = output_repo_dir / "repo_signatures.txt"

    # если всё уже есть — пропускаем
    if (
        repo_tree_file.exists()
        and import_graph_file.exists()
        and import_graph_json_file.exists()
        and repo_signatures_file.exists()
    ):
        print(f"[SKIP] already processed: {repo_full_name}")
        return

    with tempfile.TemporaryDirectory(prefix="repo_clone_") as tmp_dir:
        clone_dir = Path(tmp_dir) / repo

        print(f"[CLONE] {repo_full_name}")
        ok = clone_repo(repo_full_name, clone_dir)
        if not ok:
            return

        try:
            # 1. repo tree
            tree_text = build_repo_tree(clone_dir, max_depth=MAX_TREE_DEPTH)
            repo_tree_file.write_text(tree_text, encoding="utf-8")

            # 2. import graph
            nodes, edges = build_import_graph(clone_dir)
            import_graph_file.write_text(
                format_import_graph_text(nodes, edges),
                encoding="utf-8",
            )
            import_graph_json_file.write_text(
                json.dumps(
                    {
                        "nodes": nodes,
                        "edges": [{"source": src, "target": dst} for src, dst in edges],
                    },
                    ensure_ascii=False,
                    indent=2,
                ),
                encoding="utf-8",
            )

            # 3. signatures-only repo text
            files = collect_repo_files(
                clone_dir,
                max_file_size=MAX_SIGNATURE_FILE_SIZE,
                max_files=MAX_SIGNATURE_FILES,
                signatures_only=True,
            )
            signatures_text = format_repo_files(files)
            repo_signatures_file.write_text(signatures_text, encoding="utf-8")

            print(f"[SAVED] {output_repo_dir}")

        except Exception as e:
            print(f"[PROCESS ERROR] {repo_full_name}: {e}")
            return

        # На всякий случай удаляем явно
        if clone_dir.exists():
            shutil.rmtree(clone_dir, ignore_errors=True)


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    with open(INPUT_CSV, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames or []

        if "repo_full_name" in fieldnames:
            repo_col = "repo_full_name"
        elif "full_name" in fieldnames:
            repo_col = "full_name"
        else:
            raise ValueError("В CSV нет колонки 'repo_full_name' или 'full_name'.")

        rows = list(reader)

    total = len(rows)
    print(f"Found {total} repositories")

    for idx, row in enumerate(rows, start=1):
        repo_full_name = (row.get(repo_col) or "").strip()
        if not repo_full_name:
            print(f"[{idx}/{total}] empty repo name, skip")
            continue

        print(f"\n[{idx}/{total}] Processing {repo_full_name}")
        process_repo(repo_full_name)


if __name__ == "__main__":
    main()

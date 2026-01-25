from pathlib import Path
import ast
from typing import Dict
import re
import json

EXCLUDED_DIRS = {
    ".git",
    ".venv",
    "__pycache__",
    "node_modules",
    ".mypy_cache",
    ".pytest_cache",
    "dist",
    "build",
}

def build_repo_tree(root: Path, max_depth: int = 6) -> str:
    """
    Build ASCII tree of repository structure.
    """

    lines = []

    def walk(dir_path: Path, prefix: str = "", depth: int = 0):
        if depth > max_depth:
            return

        entries = sorted(
            [p for p in dir_path.iterdir() if p.name not in EXCLUDED_DIRS],
            key=lambda p: (p.is_file(), p.name.lower()),
        )

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
            lines.append(ast.get_source_segment(source, node))

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

        elif isinstance(node, ast.FunctionDef):
            args = ast.get_source_segment(source, node.args)
            lines.append(f"\ndef {node.name}{args}: ...")

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

        if path.suffix.lower() not in {
            ".py",
            # ".md",
            # ".txt",
            # ".json",
            # ".yaml",
            # ".yml",
            # ".toml",
            # ".ini",
        }:
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

def extract_first_json(text: str):
    match = re.search(r"(\{.*\}|\[.*\])", text, re.DOTALL)
    if not match:
        return text

    candidate = match.group(1)
    return json.loads(candidate)


def safe_llm_json(response: str) -> str:
    """
    Always returns a VALID JSON STRING.
    Never returns Python repr.
    """
    if not response:
        return "{}"

    response = response.strip()

    # 1. Try direct parse
    try:
        obj = json.loads(response)
    except json.JSONDecodeError:
        # 2. Try extract JSON from text
        obj = extract_first_json(response)

    if obj is None:
        return "{}"

    # 3. Serialize correctly
    return json.dumps(
        obj,
        ensure_ascii=False,
        indent=2,
    )
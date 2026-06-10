"""Filesystem helpers for serving Markdown content safely.

Provides safe path resolution (no traversal outside the configured roots),
listing, and reading of Markdown files under ``DOCS_DIR`` and ``PROMPTS_DIR``.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .config import ALLOWED_EXTENSIONS, DOCS_DIR, PROMPTS_DIR


class ContentError(Exception):
    """Raised when content cannot be located or a path is invalid."""


@dataclass(frozen=True)
class DocEntry:
    """Metadata about a single Markdown document."""

    path: str  # POSIX relative path from its root
    title: str
    bytes: int

    def as_dict(self) -> dict[str, object]:
        return {"path": self.path, "title": self.title, "bytes": self.bytes}


def _is_allowed(path: Path) -> bool:
    return path.suffix.lower() in ALLOWED_EXTENSIONS


def safe_resolve(root: Path, relative_path: str) -> Path:
    """Resolve ``relative_path`` against ``root``, rejecting traversal.

    Raises ``ContentError`` if the path escapes ``root``, is absolute, has a
    disallowed extension, or does not exist as a regular file.
    """

    if relative_path is None:
        raise ContentError("No path provided.")

    candidate = (root / relative_path).resolve()
    root_resolved = root.resolve()

    # Ensure the resolved path stays within the root (defeats `..`, symlinks).
    if root_resolved != candidate and root_resolved not in candidate.parents:
        raise ContentError(f"Path escapes the content root: {relative_path!r}")

    if not _is_allowed(candidate):
        allowed = ", ".join(ALLOWED_EXTENSIONS)
        raise ContentError(
            f"Only these extensions are served: {allowed} (got {candidate.suffix!r})"
        )

    if not candidate.is_file():
        raise ContentError(f"File not found: {relative_path!r}")

    return candidate


def _derive_title(path: Path) -> str:
    """Derive a human title: first Markdown heading, else the file stem."""

    try:
        with path.open("r", encoding="utf-8", errors="replace") as handle:
            for _ in range(200):  # only scan the first lines
                line = handle.readline()
                if not line:
                    break
                stripped = line.strip()
                if stripped.startswith("#"):
                    return stripped.lstrip("#").strip() or path.stem
    except OSError:
        pass
    return path.stem


def list_markdown(root: Path) -> list[DocEntry]:
    """List all Markdown files under ``root`` (recursively), sorted by path."""

    if not root.exists():
        return []

    entries: list[DocEntry] = []
    for file_path in sorted(root.rglob("*")):
        if not file_path.is_file() or not _is_allowed(file_path):
            continue
        try:
            rel = file_path.relative_to(root).as_posix()
            size = file_path.stat().st_size
        except (OSError, ValueError):
            continue
        entries.append(DocEntry(path=rel, title=_derive_title(file_path), bytes=size))
    return entries


def read_markdown(root: Path, relative_path: str) -> str:
    """Read and return the text of a Markdown file under ``root``."""

    path = safe_resolve(root, relative_path)
    return path.read_text(encoding="utf-8", errors="replace")


def read_lines_around(
    root: Path, relative_path: str, line: int, radius: int = 10
) -> dict[str, object]:
    """Return lines surrounding ``line`` (1-based) in a Markdown file.

    Returns a dict with ``path``, ``line``, ``start_line``, ``end_line``,
    and ``text`` — the joined lines of the window.
    """
    path = safe_resolve(root, relative_path)
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    start = max(0, line - 1 - radius)
    end = min(len(lines), line + radius)
    return {
        "path": relative_path,
        "line": line,
        "start_line": start + 1,
        "end_line": end,
        "text": "\n".join(lines[start:end]),
    }


# Convenience wrappers for the docs root ----------------------------------


def list_docs() -> list[DocEntry]:
    return list_markdown(DOCS_DIR)


def read_doc(relative_path: str) -> str:
    return read_markdown(DOCS_DIR, relative_path)


def list_prompt_files() -> list[DocEntry]:
    return list_markdown(PROMPTS_DIR)


def read_prompt_file(relative_path: str) -> str:
    return read_markdown(PROMPTS_DIR, relative_path)

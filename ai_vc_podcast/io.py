from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Report:
    path: Path
    title: str
    date: str
    summary: str


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_bytes(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)


def title_from_markdown(markdown: str, fallback: str) -> str:
    for line in markdown.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return fallback


def summary_from_markdown(markdown: str) -> str:
    for line in markdown.splitlines():
        stripped = line.strip()
        if stripped and not stripped.startswith("#") and not stripped.startswith("-"):
            return stripped[:320]
    return ""


def load_reports(reports_dir: Path) -> list[Report]:
    reports = []
    for path in sorted(reports_dir.glob("*.md"), reverse=True):
        markdown = read_text(path)
        stem = path.stem
        date = stem[:16] if len(stem) >= 16 else stem
        reports.append(
            Report(
                path=path,
                title=title_from_markdown(markdown, stem),
                date=date,
                summary=summary_from_markdown(markdown),
            )
        )
    return reports

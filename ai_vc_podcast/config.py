from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass
from pathlib import Path

LANGUAGE_OPTIONS = {
    "zh": ("zh-cn", "Chinese", "用中文生成最终简报。"),
    "en": ("en-us", "English", "Write the final briefing in English."),
    "es": ("es-es", "Spanish", "Escribe el informe final en español."),
}
SLUG_RE = re.compile(r"^[a-z0-9][a-z0-9-]{0,62}$")
LOCAL_TIME_RE = re.compile(r"^([01]\d|2[0-3]):([0-5]\d)$")


@dataclass(frozen=True)
class PodcastConfig:
    podcast_title: str
    podcast_description: str
    output_language: str
    category: str
    explicit: bool
    episode_slug: str
    prompt_path: str
    timezone: str
    local_run_time: str


DEFAULT_CONFIG = PodcastConfig(
    podcast_title="AI VC Morning Brief",
    podcast_description="Daily Chinese briefings on AI, VC, AI infrastructure, agents, robotics, Physical AI, startup funding, and Silicon Valley technology news.",
    output_language="zh",
    category="Business",
    explicit=False,
    episode_slug="ai-vc-daily",
    prompt_path="prompts/ai_vc_morning_brief.zh.md",
    timezone="America/Los_Angeles",
    local_run_time="07:50",
)


def load_config(project_dir: Path) -> PodcastConfig:
    path = project_dir / "podcast_config.json"
    data = DEFAULT_CONFIG.__dict__.copy()
    if path.exists():
        data.update(json.loads(path.read_text(encoding="utf-8")))

    if os.environ.get("PODCAST_TITLE"):
        data["podcast_title"] = os.environ["PODCAST_TITLE"]
    if os.environ.get("PODCAST_DESCRIPTION"):
        data["podcast_description"] = os.environ["PODCAST_DESCRIPTION"]
    if "language" in data and "output_language" not in data:
        data["output_language"] = data.pop("language")
    else:
        data.pop("language", None)

    if os.environ.get("OUTPUT_LANGUAGE"):
        data["output_language"] = os.environ["OUTPUT_LANGUAGE"]
    if os.environ.get("PODCAST_CATEGORY"):
        data["category"] = os.environ["PODCAST_CATEGORY"]
    if os.environ.get("PODCAST_EXPLICIT"):
        data["explicit"] = parse_bool(os.environ["PODCAST_EXPLICIT"])
    if os.environ.get("EPISODE_SLUG"):
        data["episode_slug"] = os.environ["EPISODE_SLUG"]
    if os.environ.get("PROMPT_PATH"):
        data["prompt_path"] = os.environ["PROMPT_PATH"]
    if os.environ.get("PODCAST_TIMEZONE"):
        data["timezone"] = os.environ["PODCAST_TIMEZONE"]
    if os.environ.get("PODCAST_LOCAL_RUN_TIME"):
        data["local_run_time"] = os.environ["PODCAST_LOCAL_RUN_TIME"]

    data["output_language"] = str(data["output_language"]).lower()
    config = PodcastConfig(**data)
    validate_config(config, project_dir)
    return config


def parse_bool(value: str) -> bool:
    normalized = value.strip().lower()
    if normalized in {"true", "1", "yes", "y"}:
        return True
    if normalized in {"false", "0", "no", "n"}:
        return False
    raise ValueError("PODCAST_EXPLICIT must be true or false.")


def validate_config(config: PodcastConfig, project_dir: Path) -> None:
    validate_language(config.output_language)
    if not config.podcast_title.strip():
        raise ValueError("podcast_title is required.")
    if not config.podcast_description.strip():
        raise ValueError("podcast_description is required.")
    if not isinstance(config.explicit, bool):
        raise ValueError("explicit must be a boolean.")
    if not SLUG_RE.fullmatch(config.episode_slug):
        raise ValueError("episode_slug must use lowercase letters, numbers, and hyphens only.")
    match = LOCAL_TIME_RE.fullmatch(config.local_run_time)
    if not match:
        raise ValueError("local_run_time must use HH:MM in 24-hour format.")
    if int(match.group(2)) % 10 != 0:
        raise ValueError("local_run_time must be on a 10-minute boundary.")
    prompt_path = Path(config.prompt_path)
    if prompt_path.is_absolute() or ".." in prompt_path.parts:
        raise ValueError("prompt_path must be a safe relative path inside the project.")
    resolved_prompt = (project_dir / prompt_path).resolve()
    resolved_root = project_dir.resolve()
    if resolved_root not in resolved_prompt.parents and resolved_prompt != resolved_root:
        raise ValueError("prompt_path must stay inside the project.")
    if not resolved_prompt.exists():
        raise ValueError(f"prompt_path does not exist: {config.prompt_path}")


def validate_language(language: str) -> None:
    if language not in LANGUAGE_OPTIONS:
        allowed = ", ".join(sorted(LANGUAGE_OPTIONS))
        raise ValueError(f"Unsupported output_language: {language}. Use one of: {allowed}.")


def rss_language(language: str) -> str:
    validate_language(language)
    return LANGUAGE_OPTIONS[language][0]


def language_prompt_instruction(language: str) -> str:
    validate_language(language)
    return LANGUAGE_OPTIONS[language][2]

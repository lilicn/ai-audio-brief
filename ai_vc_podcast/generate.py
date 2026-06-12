from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path

from .config import PodcastConfig, language_prompt_instruction, load_config
from .io import read_text, write_bytes, write_text
from .openai_client import OpenAIClient

MARKDOWN_IMAGE_RE = re.compile(r"!\[[^\]]*\]\([^)]+\)")
MARKDOWN_LINK_RE = re.compile(r"\[([^\]]+)\]\((https?://[^)]+)\)")
MARKDOWN_TOKEN_RE = re.compile(r"[*_`>#]")


def episode_stem(now: datetime | None = None, episode_slug: str = "ai-vc-daily") -> str:
    now = now or datetime.now().astimezone()
    return f"{now.strftime('%Y-%m-%d-%H%M')}-{episode_slug}"


def markdown_to_spoken_text(markdown: str, max_chars: int = 12000) -> str:
    lines = []
    for raw_line in markdown.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        line = MARKDOWN_IMAGE_RE.sub("", line)
        line = MARKDOWN_LINK_RE.sub(r"\1", line)
        line = MARKDOWN_TOKEN_RE.sub("", line)
        line = re.sub(r"^-+\s*", "", line)
        line = re.sub(r"\s+", " ", line).strip()
        if line:
            lines.append(line)
        if len("\n".join(lines)) >= max_chars:
            break
    return "\n".join(lines)[:max_chars].strip()


def generate_all(project_dir: Path, client: OpenAIClient | None = None, config: PodcastConfig | None = None) -> tuple[Path, Path, Path]:
    client = client or OpenAIClient()
    config = config or load_config(project_dir)
    prompt = read_text(project_dir / config.prompt_path)
    prompt = f"{prompt.strip()}\n\nOutput language instruction: {language_prompt_instruction(config.output_language)}\n"
    markdown = client.generate_brief(prompt)
    if not markdown.strip():
        raise RuntimeError("Generated briefing is empty.")
    stem = episode_stem(episode_slug=config.episode_slug)
    report_path = project_dir / "reports" / f"{stem}.md"
    transcript_path = project_dir / "podcast" / f"{stem}.txt"
    audio_path = project_dir / "site" / "audio" / f"{stem}.mp3"
    write_text(report_path, markdown)
    spoken = markdown_to_spoken_text(markdown)
    if not spoken:
        raise RuntimeError("Generated transcript is empty.")
    write_text(transcript_path, spoken)
    audio = client.generate_speech_mp3(spoken)
    if not audio:
        raise RuntimeError("Generated audio is empty.")
    write_bytes(audio_path, audio)
    return report_path, transcript_path, audio_path

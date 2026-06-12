from __future__ import annotations

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from .config import PodcastConfig


def should_run(config: PodcastConfig, now: datetime | None = None, window_minutes: int = 10) -> bool:
    local_now = now.astimezone(ZoneInfo(config.timezone)) if now else datetime.now(ZoneInfo(config.timezone))
    hour, minute = [int(part) for part in config.local_run_time.split(":", 1)]
    target = local_now.replace(hour=hour, minute=minute, second=0, microsecond=0)
    return target <= local_now < target + timedelta(minutes=window_minutes)

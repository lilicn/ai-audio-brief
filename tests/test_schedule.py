from __future__ import annotations

import unittest
from datetime import datetime
from zoneinfo import ZoneInfo

from ai_vc_podcast.config import PodcastConfig
from ai_vc_podcast.schedule import should_run


class ScheduleTests(unittest.TestCase):
    def test_should_run_accepts_ten_minute_window(self) -> None:
        config = PodcastConfig(
            podcast_title="Test",
            podcast_description="Test",
            output_language="zh",
            category="News",
            explicit=False,
            episode_slug="daily",
            prompt_path="prompts/test.md",
            timezone="America/Los_Angeles",
            local_run_time="07:50",
        )

        self.assertTrue(should_run(config, datetime(2026, 6, 12, 7, 50, tzinfo=ZoneInfo("America/Los_Angeles"))))
        self.assertTrue(should_run(config, datetime(2026, 6, 12, 7, 59, tzinfo=ZoneInfo("America/Los_Angeles"))))
        self.assertFalse(should_run(config, datetime(2026, 6, 12, 8, 0, tzinfo=ZoneInfo("America/Los_Angeles"))))


if __name__ == "__main__":
    unittest.main()

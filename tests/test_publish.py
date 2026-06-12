from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from ai_vc_podcast.config import PodcastConfig
from ai_vc_podcast.publish import publish


class PublishTests(unittest.TestCase):
    def test_publish_creates_pages_and_podcast_feed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            reports = root / "reports"
            audio = root / "site" / "audio"
            reports.mkdir()
            audio.mkdir(parents=True)
            (reports / "2026-06-12-0750-ai-vc-daily.md").write_text("# 简报\n\n摘要", encoding="utf-8")
            (audio / "2026-06-12-0750-ai-vc-daily.mp3").write_bytes(b"mp3")

            config = PodcastConfig(
                podcast_title="Reusable Daily Brief",
                podcast_description="Reusable description",
                output_language="en",
                category="News",
                explicit=False,
                episode_slug="daily-brief",
                prompt_path="prompts/test.md",
                timezone="UTC",
                local_run_time="08:00",
            )

            outputs = publish(root, "https://example.com/show", "owner@example.com", config)

            self.assertIn(root / "site" / "index.html", outputs)
            feed = (root / "site" / "podcast.xml").read_text(encoding="utf-8")
            self.assertIn("<title>Reusable Daily Brief</title>", feed)
            self.assertIn("<language>en-us</language>", feed)
            self.assertIn('<itunes:category text="News" />', feed)
            self.assertIn("https://example.com/show/audio/2026-06-12-0750-ai-vc-daily.mp3", feed)
            self.assertIn("<itunes:email>owner@example.com</itunes:email>", feed)
            html = (root / "site" / "index.html").read_text(encoding="utf-8")
            self.assertIn('<html lang="en-us">', html)


if __name__ == "__main__":
    unittest.main()

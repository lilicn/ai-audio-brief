from __future__ import annotations

import io
import tempfile
import unittest
import urllib.error
from pathlib import Path
from unittest.mock import patch

from ai_vc_podcast.config import PodcastConfig
from ai_vc_podcast.generate import episode_stem, generate_all, markdown_to_spoken_text
from ai_vc_podcast.openai_client import OpenAIClient, extract_text


class FakeClient:
    last_prompt = ""

    def generate_brief(self, prompt: str) -> str:
        self.last_prompt = prompt
        return "# 今日 AI VC 简报\n\n过去 24 小时重点：[Reuters](https://example.com)。"

    def generate_speech_mp3(self, text: str) -> bytes:
        return b"mp3"


class EmptyBriefClient(FakeClient):
    def generate_brief(self, prompt: str) -> str:
        return ""


class EmptyAudioClient(FakeClient):
    def generate_speech_mp3(self, text: str) -> bytes:
        return b""


class FakeResponse:
    def __init__(self, body: bytes) -> None:
        self.body = body

    def __enter__(self) -> "FakeResponse":
        return self

    def __exit__(self, *_args) -> None:  # type: ignore[no-untyped-def]
        return None

    def read(self) -> bytes:
        return self.body


class GenerateTests(unittest.TestCase):
    def test_extract_text_supports_output_text(self) -> None:
        self.assertEqual(extract_text({"output_text": "hello"}), "hello")

    def test_openai_client_uses_defaults_when_optional_env_is_empty(self) -> None:
        calls = []

        class Client(OpenAIClient):
            def __init__(self) -> None:
                self.api_key = "test"

            def _request_json(self, url, payload):  # type: ignore[no-untyped-def]
                calls.append(payload)
                return {"output_text": "brief"}

            def _request_bytes(self, url, payload):  # type: ignore[no-untyped-def]
                calls.append(payload)
                return b"mp3"

        with patch.dict(
            "os.environ",
            {
                "OPENAI_TEXT_MODEL": "",
                "OPENAI_WEB_SEARCH_TOOL": "",
                "OPENAI_TTS_MODEL": "",
                "OPENAI_TTS_VOICE": "",
            },
            clear=False,
        ):
            client = Client()
            client.generate_brief("prompt")
            client.generate_speech_mp3("text")

        self.assertEqual(calls[0]["model"], "gpt-4.1-mini")
        self.assertEqual(calls[0]["tools"], [{"type": "web_search"}])
        self.assertEqual(calls[0]["tool_choice"], "required")
        self.assertEqual(calls[1]["model"], "gpt-4o-mini-tts")
        self.assertEqual(calls[1]["voice"], "alloy")

    def test_openai_client_retries_rate_limits(self) -> None:
        rate_limit = urllib.error.HTTPError(
            url="https://api.openai.com/v1/audio/speech",
            code=429,
            msg="Too Many Requests",
            hdrs={"Retry-After": "0"},
            fp=io.BytesIO(b'{"error":{"message":"rate limited"}}'),
        )

        client = OpenAIClient(api_key="test")
        with patch("urllib.request.urlopen", side_effect=[rate_limit, FakeResponse(b"mp3")]) as urlopen:
            with patch("time.sleep") as sleep:
                audio = client.generate_speech_mp3("text")

        self.assertEqual(audio, b"mp3")
        self.assertEqual(urlopen.call_count, 2)
        sleep.assert_called_once_with(0.0)

    def test_markdown_to_spoken_text_removes_urls(self) -> None:
        spoken = markdown_to_spoken_text("# 标题\n\n[Reuters](https://example.com)")

        self.assertIn("Reuters", spoken)
        self.assertNotIn("https://example.com", spoken)

    def test_episode_stem_uses_timestamp(self) -> None:
        self.assertRegex(episode_stem(), r"20\d{2}-\d{2}-\d{2}-\d{4}-ai-vc-daily")

    def test_episode_stem_uses_custom_slug(self) -> None:
        self.assertRegex(episode_stem(episode_slug="daily-news"), r"20\d{2}-\d{2}-\d{2}-\d{4}-daily-news")

    def test_generate_all_writes_report_transcript_and_mp3(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            prompts = root / "prompts"
            prompts.mkdir()
            (prompts / "ai_vc_morning_brief.zh.md").write_text("prompt", encoding="utf-8")

            config = PodcastConfig(
                podcast_title="Test Brief",
                podcast_description="Test",
                output_language="en",
                category="News",
                explicit=False,
                episode_slug="daily-news",
                prompt_path="prompts/ai_vc_morning_brief.zh.md",
                timezone="America/Los_Angeles",
                local_run_time="07:50",
            )

            report, transcript, audio = generate_all(root, FakeClient(), config)  # type: ignore[arg-type]

            self.assertTrue(report.exists())
            self.assertIn("daily-news", report.name)
            self.assertTrue(transcript.exists())
            self.assertEqual(audio.read_bytes(), b"mp3")

    def test_generate_all_injects_language_instruction(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            prompts = root / "prompts"
            prompts.mkdir()
            (prompts / "ai_vc_morning_brief.zh.md").write_text("prompt", encoding="utf-8")
            client = FakeClient()
            config = PodcastConfig(
                podcast_title="Test Brief",
                podcast_description="Test",
                output_language="es",
                category="News",
                explicit=False,
                episode_slug="daily-news",
                prompt_path="prompts/ai_vc_morning_brief.zh.md",
                timezone="America/Los_Angeles",
                local_run_time="07:50",
            )

            generate_all(root, client, config)  # type: ignore[arg-type]

            self.assertIn("español", client.last_prompt)

    def test_generate_all_rejects_empty_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            prompts = root / "prompts"
            prompts.mkdir()
            (prompts / "ai_vc_morning_brief.zh.md").write_text("prompt", encoding="utf-8")
            config = PodcastConfig(
                podcast_title="Test Brief",
                podcast_description="Test",
                output_language="zh",
                category="News",
                explicit=False,
                episode_slug="daily-news",
                prompt_path="prompts/ai_vc_morning_brief.zh.md",
                timezone="America/Los_Angeles",
                local_run_time="07:50",
            )

            with self.assertRaises(RuntimeError):
                generate_all(root, EmptyBriefClient(), config)  # type: ignore[arg-type]
            with self.assertRaises(RuntimeError):
                generate_all(root, EmptyAudioClient(), config)  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()

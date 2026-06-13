from __future__ import annotations

import unittest
from pathlib import Path
from unittest.mock import patch

from ai_vc_podcast.config import language_prompt_instruction, load_config, parse_bool, rss_language
from ai_vc_podcast.cli import env_or_default


class ProjectHygieneTests(unittest.TestCase):
    def test_prompt_contains_required_scope(self) -> None:
        root = Path(__file__).resolve().parents[1]
        prompt = (root / "prompts" / "ai_vc_morning_brief.zh.md").read_text(encoding="utf-8")

        self.assertIn("过去 24小时", prompt)
        self.assertIn("AI Infra", prompt)
        self.assertIn("Physical AI", prompt)
        self.assertIn("VC 钱正在流向哪里", prompt)
        self.assertIn("Reuters", prompt)

    def test_no_local_private_paths_or_old_bundle_ids(self) -> None:
        root = Path(__file__).resolve().parents[1]
        forbidden = ["/User" + "s/", "com." + "wei", "OPENAI_API_KEY" + "=", "sk" + "-"]
        for path in root.rglob("*"):
            if not path.is_file() or ".git" in path.parts:
                continue
            relative_parts = path.relative_to(root).parts
            if relative_parts and relative_parts[0] in {"reports", "podcast", "site"}:
                continue
            if path.suffix in {".mp3", ".pyc"}:
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
            for token in forbidden:
                self.assertNotIn(token, text, f"{token} found in {path}")

    def test_workflow_uses_secrets_and_pages(self) -> None:
        root = Path(__file__).resolve().parents[1]
        workflow = (root / ".github" / "workflows" / "daily-podcast.yml").read_text(encoding="utf-8")

        self.assertIn("secrets.OPENAI_API_KEY", workflow)
        self.assertIn('FORCE_JAVASCRIPT_ACTIONS_TO_NODE24: "true"', workflow)
        self.assertIn("actions/deploy-pages@v4", workflow)
        self.assertIn("cron: \"*/10 * * * *\"", workflow)
        self.assertIn("python -m ai_vc_podcast should-run", workflow)
        self.assertIn("PROMPT_PATH: ${{ vars.PROMPT_PATH }}", workflow)
        self.assertIn("EPISODE_SLUG: ${{ vars.EPISODE_SLUG }}", workflow)
        self.assertIn("PODCAST_LOCAL_RUN_TIME: ${{ vars.PODCAST_LOCAL_RUN_TIME }}", workflow)
        self.assertIn("OUTPUT_LANGUAGE: ${{ vars.OUTPUT_LANGUAGE }}", workflow)
        self.assertNotIn("OWNER_EMAIL: owner@example.com", workflow)

    def test_public_config_makes_project_reusable(self) -> None:
        root = Path(__file__).resolve().parents[1]
        config = load_config(root)

        self.assertEqual(config.podcast_title, "AI VC Morning Brief")
        self.assertEqual(config.prompt_path, "prompts/ai_vc_morning_brief.zh.md")
        self.assertEqual(config.timezone, "America/Los_Angeles")
        self.assertEqual(config.local_run_time, "07:50")
        self.assertTrue((root / "podcast_config.json").exists())

    def test_environment_variables_can_override_reusable_config(self) -> None:
        root = Path(__file__).resolve().parents[1]
        with patch.dict(
            "os.environ",
            {
                "PODCAST_TITLE": "Health AI Daily Brief",
                "PODCAST_DESCRIPTION": "Health AI updates",
                "OUTPUT_LANGUAGE": "en",
                "PODCAST_CATEGORY": "Technology",
                "PODCAST_EXPLICIT": "true",
                "EPISODE_SLUG": "health-ai-daily",
                "PROMPT_PATH": "prompts/examples/health_ai.zh.md",
                "PODCAST_TIMEZONE": "UTC",
                "PODCAST_LOCAL_RUN_TIME": "08:00",
            },
            clear=False,
        ):
            config = load_config(root)

        self.assertEqual(config.podcast_title, "Health AI Daily Brief")
        self.assertEqual(config.podcast_description, "Health AI updates")
        self.assertEqual(config.output_language, "en")
        self.assertEqual(config.category, "Technology")
        self.assertTrue(config.explicit)
        self.assertEqual(config.episode_slug, "health-ai-daily")
        self.assertEqual(config.prompt_path, "prompts/examples/health_ai.zh.md")
        self.assertEqual(config.timezone, "UTC")
        self.assertEqual(config.local_run_time, "08:00")

    def test_language_options_are_limited_and_mapped(self) -> None:
        self.assertEqual(rss_language("zh"), "zh-cn")
        self.assertEqual(rss_language("en"), "en-us")
        self.assertEqual(rss_language("es"), "es-es")
        self.assertIn("中文", language_prompt_instruction("zh"))
        self.assertIn("English", language_prompt_instruction("en"))
        self.assertIn("español", language_prompt_instruction("es"))

        with self.assertRaises(ValueError):
            rss_language("fr")

    def test_config_rejects_unsafe_values(self) -> None:
        root = Path(__file__).resolve().parents[1]
        cases = [
            {"EPISODE_SLUG": "../bad"},
            {"PROMPT_PATH": "../secret.md"},
            {"PROMPT_PATH": "prompts/missing.md"},
            {"PODCAST_LOCAL_RUN_TIME": "07:55"},
            {"PODCAST_LOCAL_RUN_TIME": "25:00"},
            {"OUTPUT_LANGUAGE": "fr"},
        ]

        for env in cases:
            with self.subTest(env=env):
                with patch.dict("os.environ", env, clear=False):
                    with self.assertRaises(ValueError):
                        load_config(root)

    def test_parse_bool_is_strict(self) -> None:
        self.assertTrue(parse_bool("true"))
        self.assertFalse(parse_bool("false"))
        with self.assertRaises(ValueError):
            parse_bool("maybe")

    def test_empty_environment_values_fall_back_to_defaults(self) -> None:
        with patch.dict("os.environ", {"OWNER_EMAIL": ""}, clear=False):
            self.assertEqual(env_or_default("OWNER_EMAIL", "podcast-owner@example.com"), "podcast-owner@example.com")

    def test_prompt_templates_and_examples_exist(self) -> None:
        root = Path(__file__).resolve().parents[1]
        paths = [
            root / "prompts" / "templates" / "daily_news_brief.zh.md",
            root / "prompts" / "examples" / "parenting_trends.zh.md",
            root / "prompts" / "examples" / "health_ai.zh.md",
            root / "prompts" / "examples" / "creator_economy.zh.md",
        ]

        for path in paths:
            self.assertTrue(path.exists(), str(path))
            self.assertIn("音频", path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()

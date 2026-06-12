from __future__ import annotations

import unittest
from pathlib import Path


class StructureTests(unittest.TestCase):
    def test_template_structure_contains_required_files(self) -> None:
        root = Path(__file__).resolve().parents[1]
        required_files = [
            ".github/workflows/daily-podcast.yml",
            ".gitignore",
            "README.md",
            "podcast_config.json",
            "pyproject.toml",
            "site/.nojekyll",
            "ai_vc_podcast/__main__.py",
            "ai_vc_podcast/cli.py",
            "ai_vc_podcast/config.py",
            "ai_vc_podcast/generate.py",
            "ai_vc_podcast/io.py",
            "ai_vc_podcast/openai_client.py",
            "ai_vc_podcast/publish.py",
            "ai_vc_podcast/schedule.py",
            "docs/configuration.md",
            "docs/reuse.md",
            "prompts/ai_vc_morning_brief.zh.md",
            "prompts/templates/daily_news_brief.zh.md",
            "prompts/examples/creator_economy.zh.md",
            "prompts/examples/health_ai.zh.md",
            "prompts/examples/parenting_trends.zh.md",
        ]

        for relative_path in required_files:
            self.assertTrue((root / relative_path).is_file(), relative_path)

    def test_template_has_no_generated_or_os_junk_files(self) -> None:
        root = Path(__file__).resolve().parents[1]
        forbidden_names = {".DS_Store", "__pycache__"}
        forbidden_suffixes = {".pyc"}

        for path in root.rglob("*"):
            self.assertNotIn(path.name, forbidden_names, str(path))
            self.assertNotIn(path.suffix, forbidden_suffixes, str(path))

    def test_readme_is_bilingual_with_english_default(self) -> None:
        root = Path(__file__).resolve().parents[1]
        readme = (root / "README.md").read_text(encoding="utf-8")

        self.assertIn("[English](#english) | [中文](#中文)", readme)
        self.assertIn("## English", readme)
        self.assertIn("## 中文", readme)
        self.assertLess(readme.index("## English"), readme.index("## 中文"))
        self.assertIn("AI Audio Brief is a reusable GitHub Actions template", readme)
        self.assertIn("AI Audio Brief 是一个可复用的 GitHub Actions 模板", readme)


if __name__ == "__main__":
    unittest.main()

# Reuse Guide

This repository is designed to be forked and reused for different podcast domains.

## Minimal Changes

Change `podcast_config.json`:

```json
{
  "podcast_title": "My Daily Brief",
  "podcast_description": "A short daily audio briefing.",
  "output_language": "zh",
  "episode_slug": "daily-brief",
  "prompt_path": "prompts/my_prompt.md",
  "timezone": "America/Los_Angeles",
  "local_run_time": "07:50"
}
```

Add your prompt file under `prompts/`.

You can start from:

```text
prompts/templates/daily_news_brief.zh.md
prompts/examples/parenting_trends.zh.md
prompts/examples/health_ai.zh.md
prompts/examples/creator_economy.zh.md
```

Set GitHub Secrets:

```text
OPENAI_API_KEY
OWNER_EMAIL
```

Set GitHub Variables:

```text
SITE_URL
```

Optional GitHub Variables:

```text
PODCAST_TITLE
PODCAST_DESCRIPTION
OUTPUT_LANGUAGE
PODCAST_CATEGORY
PODCAST_EXPLICIT
EPISODE_SLUG
PROMPT_PATH
PODCAST_TIMEZONE
PODCAST_LOCAL_RUN_TIME
OPENAI_TEXT_MODEL
OPENAI_WEB_SEARCH_TOOL
OPENAI_TTS_MODEL
OPENAI_TTS_VOICE
```

Enable GitHub Pages with GitHub Actions as the source.

The workflow is configured to check the configured local time every 10 minutes. Use a `local_run_time` value on a 10-minute boundary.

## Example: Use A Different Domain

To make a health AI podcast without editing code, set:

```text
PROMPT_PATH=prompts/examples/health_ai.zh.md
PODCAST_TITLE=Health AI Daily Brief
PODCAST_DESCRIPTION=Daily Chinese briefings on health AI and digital health.
OUTPUT_LANGUAGE=zh
EPISODE_SLUG=health-ai-daily
PODCAST_CATEGORY=Technology
```

Language options:

```text
zh = Chinese
en = English
es = Spanish
```

## Public Subscription

People who only want to listen do not need to fork. They can subscribe to:

```text
https://lilicn.github.io/ai-audio-brief/podcast.xml
```

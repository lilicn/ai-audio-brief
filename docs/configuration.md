# Configuration

There are three layers of configuration.

## Public Config

Edit `podcast_config.json` for values that are safe to commit:

```json
{
  "podcast_title": "AI VC Morning Brief",
  "podcast_description": "Daily Chinese briefings...",
  "output_language": "zh",
  "category": "Business",
  "explicit": false,
  "episode_slug": "ai-vc-daily",
  "prompt_path": "prompts/ai_vc_morning_brief.zh.md",
  "timezone": "America/Los_Angeles",
  "local_run_time": "07:50"
}
```

## GitHub Secrets

Use secrets for sensitive values:

```text
OPENAI_API_KEY
OWNER_EMAIL
```

`OWNER_EMAIL` may appear in the public podcast RSS. Use a podcast-specific email address.

## GitHub Variables

Use variables to customize a fork without editing files:

```text
SITE_URL
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
OPENAI_MAX_RETRIES
OPENAI_RETRY_BASE_SECONDS
```

`OPENAI_WEB_SEARCH_TOOL` defaults to `web_search`, the current hosted web search tool for the Responses API.

`OPENAI_MAX_RETRIES` defaults to `4`. `OPENAI_RETRY_BASE_SECONDS` defaults to `2`.

`OUTPUT_LANGUAGE` supports only:

```text
zh
en
es
```

For this repo, set:

```text
SITE_URL=https://lilicn.github.io/ai-audio-brief
```

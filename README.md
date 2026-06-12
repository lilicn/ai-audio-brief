# AI Audio Brief

This is a reusable template for publishing an automated audio podcast from a text-generation prompt.

The default prompt generates a Chinese `AI VC Morning Brief`, but users can fork the repo, replace the prompt, set a few GitHub secrets, and publish their own podcast feed on GitHub Pages. It can be adapted for parenting trends, health AI, creator economy, local news, investing, research updates, and similar briefing-style domains.

## Two Ways To Use It

Subscribe to this podcast:

```text
https://lilicn.github.io/ai-audio-brief/podcast.xml
```

Fork it to run your own:

```text
fork repo
  -> edit podcast_config.json
  -> choose or write a prompt under prompts/
  -> set GitHub Secrets and Variables
  -> enable GitHub Pages
  -> run the workflow
```

## What It Does

```text
GitHub Actions scheduled run
  -> OpenAI Responses API + web search
  -> reports/YYYY-MM-DD-HHMM-<episode_slug>.md
  -> podcast/YYYY-MM-DD-HHMM-<episode_slug>.txt
  -> OpenAI text-to-speech MP3
  -> site/audio/YYYY-MM-DD-HHMM-<episode_slug>.mp3
  -> site/podcast.xml
  -> GitHub Pages
  -> Apple Podcasts or another RSS-compatible podcast app
```

## Quick Setup

1. Fork this repository.
2. In Settings -> Secrets and variables -> Actions, add secrets:

```text
OPENAI_API_KEY
OWNER_EMAIL
```

3. Add repository variables:

```text
SITE_URL=https://lilicn.github.io/ai-audio-brief
```

For a fork, replace `lilicn` and `ai-audio-brief` with your GitHub owner and repository name.

Optional variables:

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

4. In Settings -> Pages, choose **GitHub Actions** as the source.
5. Run the workflow manually once from the Actions tab.
6. Submit this feed to Apple Podcasts Connect:

```text
https://lilicn.github.io/ai-audio-brief/podcast.xml
```

## Customize

Edit public config:

```text
podcast_config.json
```

Key fields:

```json
{
  "podcast_title": "AI VC Morning Brief",
  "output_language": "zh",
  "episode_slug": "ai-vc-daily",
  "prompt_path": "prompts/ai_vc_morning_brief.zh.md",
  "timezone": "America/Los_Angeles",
  "local_run_time": "07:50"
}
```

`output_language` options:

```text
zh = Chinese
en = English
es = Spanish
```

Edit the prompt:

```text
prompts/ai_vc_morning_brief.zh.md
```

Or choose an example:

```text
prompts/templates/daily_news_brief.zh.md
prompts/examples/parenting_trends.zh.md
prompts/examples/health_ai.zh.md
prompts/examples/creator_economy.zh.md
```

To use a different prompt without editing code, set:

```text
PROMPT_PATH=prompts/examples/health_ai.zh.md
PODCAST_TITLE=Health AI Daily Brief
EPISODE_SLUG=health-ai-daily
OUTPUT_LANGUAGE=en
```

The GitHub workflow is configured to wake up every 10 minutes and checks `podcast_config.json` before doing real work. Set `local_run_time` to a 10-minute boundary such as `07:50`, `08:00`, or `08:30`.

## Local Test

```bash
python -m unittest discover -s tests
```

## Privacy

Do not commit API keys, local absolute paths, personal email addresses, or private notes. Use GitHub Secrets for sensitive values.

## More

- `docs/configuration.md`: config fields, secrets, variables, and language options.
- `docs/reuse.md`: examples for adapting the template to other domains.

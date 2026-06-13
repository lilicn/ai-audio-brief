# AI Audio Brief

[English](#english) | [中文](#中文)

## English

AI Audio Brief is a reusable GitHub Actions template that turns a text-generation prompt into an automated audio podcast.

The default prompt generates a Chinese `AI VC Morning Brief`, but users can fork the repo, replace the prompt, set a few GitHub secrets, and publish their own podcast feed on GitHub Pages. It can be adapted for parenting trends, health AI, creator economy, local news, investing, research updates, and similar briefing-style domains.

### Listen

Subscribe to this podcast:

```text
https://lilicn.github.io/ai-audio-brief/podcast.xml
```

### Run Your Own

```text
fork repo
  -> edit podcast_config.json
  -> choose or write a prompt under prompts/
  -> set GitHub Secrets and Variables
  -> enable GitHub Pages
  -> run the workflow
```

### Workflow

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

### Quick Setup

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
OPENAI_MAX_RETRIES
OPENAI_RETRY_BASE_SECONDS
```

4. In Settings -> Pages, choose **GitHub Actions** as the source.
5. Run the workflow manually once from the Actions tab.
6. Submit this feed to Apple Podcasts Connect:

```text
https://lilicn.github.io/ai-audio-brief/podcast.xml
```

### Customize

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

### Local Test

```bash
python -m unittest discover -s tests
```

### Privacy

Do not commit API keys, local absolute paths, personal email addresses, or private notes. Use GitHub Secrets for sensitive values.

### More

- `docs/configuration.md`: config fields, secrets, variables, and language options.
- `docs/reuse.md`: examples for adapting the template to other domains.

## 中文

AI Audio Brief 是一个可复用的 GitHub Actions 模板，可以把一个文本生成 prompt 自动变成音频播客。

默认 prompt 会生成中文的 `AI VC Morning Brief`，但你可以 fork 这个仓库，替换 prompt，设置少量 GitHub Secrets，然后用 GitHub Pages 发布自己的 podcast RSS。它适合改造成育儿趋势、医疗 AI、创作者经济、本地新闻、投资、研究动态等简报类音频。

### 直接订阅

订阅这个 podcast：

```text
https://lilicn.github.io/ai-audio-brief/podcast.xml
```

### 运行自己的版本

```text
fork 仓库
  -> 编辑 podcast_config.json
  -> 在 prompts/ 下选择或编写 prompt
  -> 设置 GitHub Secrets 和 Variables
  -> 启用 GitHub Pages
  -> 运行 workflow
```

### 工作流

```text
GitHub Actions 定时运行
  -> OpenAI Responses API + web search
  -> reports/YYYY-MM-DD-HHMM-<episode_slug>.md
  -> podcast/YYYY-MM-DD-HHMM-<episode_slug>.txt
  -> OpenAI text-to-speech MP3
  -> site/audio/YYYY-MM-DD-HHMM-<episode_slug>.mp3
  -> site/podcast.xml
  -> GitHub Pages
  -> Apple Podcasts 或其他兼容 RSS 的播客 App
```

### 快速设置

1. Fork 这个仓库。
2. 在 Settings -> Secrets and variables -> Actions 里添加 secrets：

```text
OPENAI_API_KEY
OWNER_EMAIL
```

3. 添加 repository variable：

```text
SITE_URL=https://lilicn.github.io/ai-audio-brief
```

如果是你自己的 fork，把 `lilicn` 和 `ai-audio-brief` 换成你的 GitHub owner 和 repo 名。

可选 variables：

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
OPENAI_MAX_RETRIES
OPENAI_RETRY_BASE_SECONDS
```

4. 在 Settings -> Pages 中选择 **GitHub Actions** 作为发布来源。
5. 在 Actions 页面手动运行一次 workflow。
6. 把这个 feed 提交到 Apple Podcasts Connect：

```text
https://lilicn.github.io/ai-audio-brief/podcast.xml
```

### 自定义

编辑公开配置：

```text
podcast_config.json
```

关键字段：

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

`output_language` 选项：

```text
zh = 中文
en = 英文
es = 西班牙语
```

编辑 prompt：

```text
prompts/ai_vc_morning_brief.zh.md
```

也可以从示例开始：

```text
prompts/templates/daily_news_brief.zh.md
prompts/examples/parenting_trends.zh.md
prompts/examples/health_ai.zh.md
prompts/examples/creator_economy.zh.md
```

不改代码切换到其他 prompt：

```text
PROMPT_PATH=prompts/examples/health_ai.zh.md
PODCAST_TITLE=Health AI Daily Brief
EPISODE_SLUG=health-ai-daily
OUTPUT_LANGUAGE=en
```

GitHub workflow 会每 10 分钟醒来检查一次 `podcast_config.json`，只有到配置的本地时间才真正生成内容。`local_run_time` 需要是 10 分钟边界，比如 `07:50`、`08:00` 或 `08:30`。

### 本地测试

```bash
python -m unittest discover -s tests
```

### 隐私

不要提交 API key、本地绝对路径、个人邮箱或私人笔记。敏感值请使用 GitHub Secrets。

### 更多

- `docs/configuration.md`：配置字段、secrets、variables 和语言选项。
- `docs/reuse.md`：如何把模板改成其他领域。

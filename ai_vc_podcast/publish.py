from __future__ import annotations

import html
import re
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote
from xml.sax.saxutils import escape as xml_escape

from .config import PodcastConfig, load_config, rss_language
from .io import Report, load_reports, read_text, write_text

LINK_RE = re.compile(r"\[([^\]]+)\]\((https?://[^)]+)\)")


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def render_inline(text: str) -> str:
    parts = []
    last = 0
    for match in LINK_RE.finditer(text):
        parts.append(html.escape(text[last : match.start()]))
        parts.append(f'<a href="{html.escape(match.group(2), quote=True)}">{html.escape(match.group(1))}</a>')
        last = match.end()
    parts.append(html.escape(text[last:]))
    return "".join(parts)


def markdown_to_html(markdown: str) -> str:
    lines = []
    for raw in markdown.splitlines():
        line = raw.strip()
        if line.startswith("# "):
            lines.append(f"<h1>{render_inline(line[2:])}</h1>")
        elif line.startswith("## "):
            lines.append(f"<h2>{render_inline(line[3:])}</h2>")
        elif line.startswith("- "):
            lines.append(f'<p class="bullet">{render_inline(line)}</p>')
        elif line:
            lines.append(f"<p>{render_inline(line)}</p>")
        else:
            lines.append("")
    return "\n".join(lines)


def page_shell(title: str, body: str, html_language: str) -> str:
    return f"""<!doctype html>
<html lang="{html.escape(html_language)}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)}</title>
  <style>
    body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; margin: 0; color: #1f2328; background: #f6f8fa; }}
    main {{ max-width: 880px; margin: 0 auto; padding: 32px 20px 64px; background: #fff; min-height: 100vh; }}
    a {{ color: #0969da; }}
    h1 {{ font-size: 32px; line-height: 1.2; }}
    h2 {{ margin-top: 32px; border-top: 1px solid #d8dee4; padding-top: 20px; }}
    p {{ line-height: 1.65; }}
    .meta, .summary {{ color: #57606a; }}
    .card {{ border: 1px solid #d8dee4; border-radius: 8px; padding: 16px; margin: 16px 0; background: #fff; }}
    .bullet {{ margin-left: 16px; }}
  </style>
</head>
<body><main>{body}</main></body>
</html>
"""


def render_index(reports: list[Report], config: PodcastConfig) -> str:
    cards = []
    for report in reports:
        html_name = quote(report.path.with_suffix(".html").name)
        cards.append(
            f"""<article class="card">
  <h2><a href="{html_name}">{html.escape(report.title)}</a></h2>
  <p class="meta">{html.escape(report.date)}</p>
  <p class="summary">{html.escape(report.summary)}</p>
</article>"""
        )
    return page_shell(
        config.podcast_title,
        f"""<h1>{html.escape(config.podcast_title)}</h1>
<p class="meta">Generated at {html.escape(now_iso())}</p>
<p><a href="podcast.xml">Podcast RSS</a></p>
{''.join(cards)}""",
        rss_language(config.output_language),
    )


def render_podcast_xml(reports: list[Report], site_url: str, owner_email: str, config: PodcastConfig) -> str:
    base = site_url.rstrip("/")
    items = []
    for report in reports[:50]:
        audio_path = report.path.parents[1] / "site" / "audio" / f"{report.path.stem}.mp3"
        if not audio_path.exists():
            continue
        audio_url = f"{base}/audio/{quote(audio_path.name)}" if base else f"audio/{quote(audio_path.name)}"
        page_url = f"{base}/{quote(report.path.with_suffix('.html').name)}" if base else quote(report.path.with_suffix(".html").name)
        items.append(
            f"""<item>
  <title>{xml_escape(report.title)}</title>
  <link>{xml_escape(page_url)}</link>
  <guid isPermaLink="false">{xml_escape(audio_url)}</guid>
  <description>{xml_escape(report.summary)}</description>
  <itunes:summary>{xml_escape(report.summary)}</itunes:summary>
  <enclosure url="{xml_escape(audio_url)}" length="{audio_path.stat().st_size}" type="audio/mpeg" />
</item>"""
        )
    return f"""<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0" xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd">
<channel>
  <title>{xml_escape(config.podcast_title)}</title>
  <link>{xml_escape(base or ".")}</link>
  <language>{xml_escape(rss_language(config.output_language))}</language>
  <description>{xml_escape(config.podcast_description)}</description>
  <itunes:author>{xml_escape(config.podcast_title)}</itunes:author>
  <itunes:owner>
    <itunes:name>{xml_escape(config.podcast_title)}</itunes:name>
    <itunes:email>{xml_escape(owner_email)}</itunes:email>
  </itunes:owner>
  <itunes:category text="{xml_escape(config.category)}" />
  <itunes:explicit>{str(config.explicit).lower()}</itunes:explicit>
  {''.join(items)}
</channel>
</rss>
"""


def publish(project_dir: Path, site_url: str, owner_email: str, config: PodcastConfig | None = None) -> list[Path]:
    config = config or load_config(project_dir)
    reports = load_reports(project_dir / "reports")
    site_dir = project_dir / "site"
    outputs: list[Path] = []
    for report in reports:
        output = site_dir / report.path.with_suffix(".html").name
        write_text(output, page_shell(report.title, markdown_to_html(read_text(report.path)), rss_language(config.output_language)))
        outputs.append(output)
    index = site_dir / "index.html"
    podcast = site_dir / "podcast.xml"
    nojekyll = site_dir / ".nojekyll"
    write_text(index, render_index(reports, config))
    write_text(podcast, render_podcast_xml(reports, site_url, owner_email, config))
    write_text(nojekyll, "")
    outputs.extend([index, podcast, nojekyll])
    return outputs

from __future__ import annotations

import argparse
import os
from pathlib import Path

from .config import load_config
from .generate import generate_all
from .publish import publish
from .schedule import should_run


def project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def env_or_default(name: str, default: str = "") -> str:
    return os.environ.get(name) or default


def main() -> int:
    parser = argparse.ArgumentParser(description="AI VC Morning Brief podcast automation")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("generate", help="Generate briefing markdown, transcript, and MP3.")

    publish_parser = subparsers.add_parser("publish", help="Generate static site and podcast RSS.")
    publish_parser.add_argument("--site-url", default=env_or_default("SITE_URL"))
    publish_parser.add_argument("--owner-email", default=env_or_default("OWNER_EMAIL", "podcast-owner@example.com"))

    subparsers.add_parser("run-all", help="Generate briefing, MP3, site, and podcast RSS.")
    subparsers.add_parser("should-run", help="Write run=true/false for GitHub Actions.")

    args = parser.parse_args()
    root = project_root()
    config = load_config(root)
    if args.command == "generate":
        for path in generate_all(root, config=config):
            print(path)
        return 0
    if args.command == "publish":
        for path in publish(root, args.site_url, args.owner_email, config):
            print(path)
        return 0
    if args.command == "run-all":
        for path in generate_all(root, config=config):
            print(path)
        for path in publish(root, env_or_default("SITE_URL"), env_or_default("OWNER_EMAIL", "podcast-owner@example.com"), config):
            print(path)
        return 0
    if args.command == "should-run":
        print(f"run={str(should_run(config)).lower()}")
        return 0
    return 2

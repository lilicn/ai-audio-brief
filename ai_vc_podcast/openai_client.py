from __future__ import annotations

import json
import os
import urllib.request
from typing import Any


class OpenAIClient:
    def __init__(self, api_key: str | None = None) -> None:
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY", "")
        if not self.api_key:
            raise RuntimeError("OPENAI_API_KEY is required.")

    def _request_json(self, url: str, payload: dict[str, Any]) -> dict[str, Any]:
        request = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        with urllib.request.urlopen(request, timeout=180) as response:
            return json.loads(response.read().decode("utf-8"))

    def _request_bytes(self, url: str, payload: dict[str, Any]) -> bytes:
        request = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        with urllib.request.urlopen(request, timeout=180) as response:
            return response.read()

    def generate_brief(self, prompt: str) -> str:
        model = os.environ.get("OPENAI_TEXT_MODEL") or "gpt-4.1-mini"
        web_search_tool = os.environ.get("OPENAI_WEB_SEARCH_TOOL") or "web_search"
        response = self._request_json(
            "https://api.openai.com/v1/responses",
            {
                "model": model,
                "tools": [{"type": web_search_tool}],
                "tool_choice": "required",
                "input": prompt,
            },
        )
        return extract_text(response)

    def generate_speech_mp3(self, text: str) -> bytes:
        model = os.environ.get("OPENAI_TTS_MODEL") or "gpt-4o-mini-tts"
        voice = os.environ.get("OPENAI_TTS_VOICE") or "alloy"
        return self._request_bytes(
            "https://api.openai.com/v1/audio/speech",
            {
                "model": model,
                "voice": voice,
                "input": text,
                "response_format": "mp3",
            },
        )


def extract_text(response: dict[str, Any]) -> str:
    if isinstance(response.get("output_text"), str):
        return response["output_text"].strip()
    parts: list[str] = []
    for item in response.get("output", []):
        for content in item.get("content", []):
            text = content.get("text")
            if isinstance(text, str):
                parts.append(text)
    text = "\n".join(parts).strip()
    if not text:
        raise RuntimeError("OpenAI response did not contain text.")
    return text

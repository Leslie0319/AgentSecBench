from __future__ import annotations

import os
import time

import httpx

from agentsecbench.adapters.base import ModelAdapter
from agentsecbench.schema import ModelRequest, ModelResponse


class OpenAICompatibleAdapter(ModelAdapter):
    """Thin HTTP adapter for authorized OpenAI-compatible endpoints."""

    def __init__(
        self,
        *,
        model: str,
        base_url: str,
        api_key_env: str | None = None,
        timeout_seconds: float = 60.0,
    ) -> None:
        self.model = model
        self.base_url = base_url.rstrip("/")
        self.api_key_env = api_key_env
        self.timeout_seconds = timeout_seconds

    def generate(self, request: ModelRequest) -> ModelResponse:
        headers: dict[str, str] = {"Content-Type": "application/json"}
        if self.api_key_env:
            api_key = os.getenv(self.api_key_env)
            if api_key:
                headers["Authorization"] = f"Bearer {api_key}"

        messages: list[dict[str, str]] = []
        if request.system_prompt:
            messages.append({"role": "system", "content": request.system_prompt})
        messages.append({"role": "user", "content": request.prompt})

        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": request.temperature,
            "max_tokens": request.max_tokens,
        }

        started = time.perf_counter()
        with httpx.Client(timeout=self.timeout_seconds) as client:
            response = client.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload,
            )
            response.raise_for_status()

        elapsed_ms = (time.perf_counter() - started) * 1000
        body = response.json()
        text = body["choices"][0]["message"]["content"]

        return ModelResponse(
            text=text,
            model=self.model,
            latency_ms=elapsed_ms,
            metadata={"backend": "openai_compatible"},
        )

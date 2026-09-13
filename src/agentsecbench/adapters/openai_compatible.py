from __future__ import annotations

import os
import time
from typing import Any

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
        trust_env: bool = True,
        request_options: dict[str, Any] | None = None,
    ) -> None:
        self.model = model
        self.base_url = base_url.rstrip("/")
        self.api_key_env = api_key_env
        self.timeout_seconds = timeout_seconds
        self.trust_env = trust_env
        self.request_options = dict(request_options or {})

    def generate(self, request: ModelRequest) -> ModelResponse:
        headers: dict[str, str] = {"Content-Type": "application/json"}
        if self.api_key_env:
            api_key = os.getenv(self.api_key_env)
            if not api_key:
                raise RuntimeError(
                    f"Missing API key environment variable: {self.api_key_env}. "
                    "Store the key locally; never commit it to Git."
                )
            headers["Authorization"] = f"Bearer {api_key}"

        messages: list[dict[str, str]] = []
        if request.system_prompt:
            messages.append({"role": "system", "content": request.system_prompt})
        messages.append({"role": "user", "content": request.prompt})

        # Provider-specific options are allowed, but core benchmark fields win so
        # configs cannot silently replace the model, messages, or generation controls.
        payload: dict[str, Any] = dict(self.request_options)
        payload.update(
            {
                "model": self.model,
                "messages": messages,
                "temperature": request.temperature,
                "max_tokens": request.max_tokens,
            }
        )

        started = time.perf_counter()
        with httpx.Client(
            timeout=self.timeout_seconds,
            trust_env=self.trust_env,
        ) as client:
            response = client.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload,
            )
            try:
                response.raise_for_status()
            except httpx.HTTPStatusError as exc:
                provider_body = response.text.strip().replace("\n", " ")[:800]
                hint = ""
                if response.status_code == 401:
                    hint = (
                        " Check that the API key is valid and belongs to the same "
                        "provider region/workspace as the configured base URL."
                    )
                raise RuntimeError(
                    f"Provider HTTP {response.status_code} for {self.base_url}: "
                    f"{provider_body or '<empty response body>'}.{hint}"
                ) from exc

        elapsed_ms = (time.perf_counter() - started) * 1000
        body = response.json()
        choice = body["choices"][0]
        text = choice["message"].get("content") or ""

        return ModelResponse(
            text=text,
            model=self.model,
            latency_ms=elapsed_ms,
            metadata={
                "backend": "openai_compatible",
                "finish_reason": choice.get("finish_reason"),
                "usage": body.get("usage"),
                "temperature": request.temperature,
                "max_tokens": request.max_tokens,
                "trust_env": self.trust_env,
                "request_options": self.request_options,
            },
        )

"""
KadiRail AI - LLM Service Layer
Connects to vLLM (OpenAI-compatible API) running on AMD Developer Cloud.
Supports AMD Instinct MI300X via ROCm.
"""

import json
import logging
import os
from dataclasses import dataclass, field
from typing import Any, Optional

import requests

logger = logging.getLogger(__name__)


@dataclass
class LLMConfig:
    """Configuration for the LLM service."""
    base_url: str = os.getenv("LLM_BASE_URL", "http://localhost:8000/v1")
    api_key: str = os.getenv("LLM_API_KEY", "EMPTY")
    model: str = os.getenv("LLM_MODEL", "Qwen/Qwen2-7B-Instruct")
    max_tokens: int = int(os.getenv("LLM_MAX_TOKENS", "2048"))
    temperature: float = float(os.getenv("LLM_TEMPERATURE", "0.7"))
    timeout: int = int(os.getenv("LLM_TIMEOUT", "120"))


class LLMService:
    """
    LLM Service that communicates with vLLM via OpenAI-compatible API.
    Designed for AMD Instinct MI300X + ROCm + vLLM stack.
    """

    def __init__(self, config: Optional[LLMConfig] = None):
        self.config = config or LLMConfig()
        self._session = requests.Session()
        self._session.headers.update({
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.config.api_key}",
        })

    @property
    def chat_url(self) -> str:
        return f"{self.config.base_url}/chat/completions"

    @property
    def models_url(self) -> str:
        return f"{self.config.base_url}/models"

    def health_check(self) -> dict:
        """Check if the LLM service is available."""
        try:
            resp = self._session.get(self.models_url, timeout=10)
            resp.raise_for_status()
            data = resp.json()
            models = [m["id"] for m in data.get("data", [])]
            return {"status": "healthy", "models": models}
        except Exception as e:
            logger.error(f"LLM health check failed: {e}")
            return {"status": "unhealthy", "error": str(e)}

    def chat(
        self,
        messages: list[dict[str, str]],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        system_prompt: Optional[str] = None,
    ) -> dict[str, Any]:
        """
        Send a chat completion request to the LLM.

        Args:
            messages: List of {"role": "user"|"assistant"|"system", "content": "..."}
            temperature: Override default temperature
            max_tokens: Override default max tokens
            system_prompt: Prepend a system message if provided

        Returns:
            {"content": str, "usage": dict, "model": str}
        """
        if system_prompt:
            messages = [{"role": "system", "content": system_prompt}] + messages

        payload = {
            "model": self.config.model,
            "messages": messages,
            "temperature": temperature or self.config.temperature,
            "max_tokens": max_tokens or self.config.max_tokens,
        }

        try:
            resp = self._session.post(
                self.chat_url,
                json=payload,
                timeout=self.config.timeout,
            )
            resp.raise_for_status()
            data = resp.json()

            choice = data["choices"][0]
            return {
                "content": choice["message"]["content"],
                "usage": data.get("usage", {}),
                "model": data.get("model", self.config.model),
                "finish_reason": choice.get("finish_reason", "unknown"),
            }

        except requests.exceptions.Timeout:
            logger.error("LLM request timed out")
            return {"content": "", "error": "timeout", "usage": {}}
        except requests.exceptions.ConnectionError:
            logger.error("Cannot connect to LLM service")
            return {"content": "", "error": "connection_failed", "usage": {}}
        except Exception as e:
            logger.error(f"LLM request failed: {e}")
            return {"content": "", "error": str(e), "usage": {}}

    def chat_simple(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """Simple chat interface — send a prompt, get a string back."""
        messages = [{"role": "user", "content": prompt}]
        result = self.chat(messages, system_prompt=system_prompt)
        return result.get("content", "")

    def chat_json(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        fallback: Optional[dict] = None,
    ) -> dict:
        """Chat and parse the response as JSON."""
        if system_prompt:
            system_prompt += "\n\nRespond with valid JSON only. No markdown, no explanation."
        else:
            system_prompt = "Respond with valid JSON only. No markdown, no explanation."

        result = self.chat_simple(prompt, system_prompt=system_prompt)

        # Try to extract JSON from response
        try:
            # Handle markdown code blocks
            if "```json" in result:
                result = result.split("```json")[1].split("```")[0]
            elif "```" in result:
                result = result.split("```")[1].split("```")[0]
            return json.loads(result.strip())
        except (json.JSONDecodeError, IndexError):
            logger.warning(f"Failed to parse LLM JSON response: {result[:200]}")
            return fallback or {}


# Singleton instance
_llm_instance: Optional[LLMService] = None


def get_llm_service(config: Optional[LLMConfig] = None) -> LLMService:
    """Get or create the LLM service singleton."""
    global _llm_instance
    if _llm_instance is None or config is not None:
        _llm_instance = LLMService(config)
    return _llm_instance

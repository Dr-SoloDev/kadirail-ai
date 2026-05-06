"""
KadiRail AI - Base Agent Class
Foundation for all specialized legal agents.
"""

import logging
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Optional

from services.llm_service import LLMService, get_llm_service

logger = logging.getLogger(__name__)


@dataclass
class AgentResult:
    """Standardized result from any agent."""
    agent_name: str
    status: str  # "success", "error", "partial"
    data: dict = field(default_factory=dict)
    reasoning: str = ""
    confidence: float = 0.0
    execution_time: float = 0.0
    error: Optional[str] = None
    token_usage: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "agent_name": self.agent_name,
            "status": self.status,
            "data": self.data,
            "reasoning": self.reasoning,
            "confidence": self.confidence,
            "execution_time": self.execution_time,
            "error": self.error,
            "token_usage": self.token_usage,
        }


class BaseAgent(ABC):
    """
    Abstract base class for all KadiRail AI agents.
    Each agent wraps a specific legal analysis capability
    and uses the LLM for intelligent processing.
    """

    def __init__(self, name: str, description: str, llm: Optional[LLMService] = None):
        self.name = name
        self.description = description
        self.llm = llm or get_llm_service()
        self._history: list[AgentResult] = []

    @property
    @abstractmethod
    def system_prompt(self) -> str:
        """System prompt that defines this agent's personality and capabilities."""
        pass

    @abstractmethod
    def execute(self, task: dict[str, Any]) -> AgentResult:
        """Execute the agent's primary task."""
        pass

    def run(self, task: dict[str, Any]) -> AgentResult:
        """Run the agent with timing and error handling."""
        start = time.time()
        try:
            logger.info(f"[{self.name}] Starting task: {task.get('action', 'unknown')}")
            result = self.execute(task)
            result.execution_time = time.time() - start
            self._history.append(result)
            logger.info(f"[{self.name}] Completed in {result.execution_time:.2f}s")
            return result
        except Exception as e:
            elapsed = time.time() - start
            logger.error(f"[{self.name}] Failed after {elapsed:.2f}s: {e}")
            result = AgentResult(
                agent_name=self.name,
                status="error",
                error=str(e),
                execution_time=elapsed,
            )
            self._history.append(result)
            return result

    def ask_llm(self, prompt: str, temperature: Optional[float] = None) -> str:
        """Send a prompt to the LLM with this agent's system prompt."""
        return self.llm.chat_simple(prompt, system_prompt=self.system_prompt)

    def ask_llm_json(self, prompt: str, fallback: Optional[dict] = None) -> dict:
        """Send a prompt to the LLM and parse JSON response."""
        return self.llm.chat_json(prompt, system_prompt=self.system_prompt, fallback=fallback)

    @property
    def history(self) -> list[dict]:
        """Get agent execution history."""
        return [r.to_dict() for r in self._history]

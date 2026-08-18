from abc import ABC, abstractmethod
from typing import Any


class BaseLLMProvider(ABC):
    @abstractmethod
    async def generate(self, prompt: str, schema: dict[str, Any] | None = None) -> dict[str, Any]:
        pass

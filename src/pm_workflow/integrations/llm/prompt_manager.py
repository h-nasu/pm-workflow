from pathlib import Path

from pm_workflow.config import get_settings


class PromptManager:
    def __init__(self):
        self.settings = get_settings()
        self.prompts_dir = Path(__file__).resolve().parent.parent.parent / "prompts"

    def load(self, name: str) -> str:
        path = self.prompts_dir / f"{name}.txt"
        if not path.exists():
            raise FileNotFoundError(f"Prompt template not found: {path}")
        return path.read_text(encoding="utf-8")

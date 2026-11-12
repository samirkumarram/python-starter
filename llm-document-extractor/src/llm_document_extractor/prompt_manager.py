from pathlib import Path
class PromptManager:
    def __init__(self, prompt_dir: Path | None = None, version: str = "v1"):
        project_root = Path(__file__).resolve().parents[2]
        self.prompt_dir = (
            prompt_dir.resolve()
            if prompt_dir is not None
            else project_root / "prompts"
        )
        if not version or Path(version).name != version or version in {".", ".."}:
            raise ValueError("Invalid prompt version.")
        self.version = version

    def load_prompt(self, document_type: str, prompt_name: str) -> str:
        if(not document_type or Path(document_type).name != document_type or document_type in {".",".."}):
            raise ValueError("Invalid document type.")
        if prompt_name not in {"system", "extraction"}:
            raise ValueError("Invalid prompt name.")
        prompt_path = (self.prompt_dir / document_type / self.version / f"{prompt_name}.txt")
        if not prompt_path.is_file():
            raise FileNotFoundError(f"Prompt file not found: {prompt_path}")
        return prompt_path.read_text(encoding="utf-8")

    def get_system_prompt(self, document_type: str) -> str:
        return self.load_prompt(document_type, "system")

    def get_extraction_prompt(self, document_type: str) -> str:
        return self.load_prompt(document_type, "extraction")
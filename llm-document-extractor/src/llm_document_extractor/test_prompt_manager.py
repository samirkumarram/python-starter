from pathlib import Path

import pytest

from llm_document_extractor.prompt_manager import PromptManager

@pytest.fixture
def prompt_manager(tmp_path: Path) -> PromptManager:
    prompts_dir = tmp_path / "prompts"
    cv_dir = prompts_dir / "cv" / "v1"
    cv_dir.mkdir(parents=True)
    (cv_dir / "system.txt").write_text("You are a CV extraction assistant.", encoding="utf-8")
    (cv_dir / "extraction.txt").write_text("Extract information from this CV:\n{document_text}", encoding="utf-8")
    return PromptManager(prompt_dir=prompts_dir)

def test_load_system_prompt(prompt_manager):
    result = prompt_manager.get_system_prompt("cv")
    assert result == "You are a CV extraction assistant."

def test_load_extraction_prompt(prompt_manager):
    result = prompt_manager.load_prompt("cv", "extraction")
    assert "{document_text}" in result

def test_get_extraction_prompt(prompt_manager):
    result = prompt_manager.get_extraction_prompt("cv")
    assert result == "Extract information from this CV:\n{document_text}"

def test_missing_prompt_file(prompt_manager):
    with pytest.raises(FileNotFoundError):
        prompt_manager.get_system_prompt("invoice")

def test_invalid_document_type(prompt_manager):
    with pytest.raises(ValueError, match="Invalid document type"):
        prompt_manager.get_system_prompt("../config")

def test_invalid_prompt_type(prompt_manager):
    with pytest.raises(ValueError, match="Invalid prompt name"):
        prompt_manager.load_prompt("cv", "unknown")
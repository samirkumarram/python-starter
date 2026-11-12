from unittest.mock import Mock
import pytest
from pydantic import ValidationError
from llm_document_extractor.schemas import CVData
from llm_document_extractor.document_extractor import DocumentExtractor

def test_extract_cv():
    llm_client = Mock()
    prompt_manager = Mock()

    prompt_manager.get_system_prompt.return_value = "CV system prompt"
    prompt_manager.get_extraction_prompt.return_value = "Extract CV details"
    llm_client.generate.return_value = '{"name": "Samir"}'
    extractor = DocumentExtractor(llm_client, prompt_manager)
    result = extractor.extract(document_type="cv", document_text="Name: Samir")
    assert result == '{"name": "Samir"}'

    prompt_manager.get_system_prompt.assert_called_once_with("cv")
    prompt_manager.get_extraction_prompt.assert_called_once_with("cv")
    llm_client.generate.assert_called_once_with(prompt=("Extract CV details\n\n"
                                                        "DOCUMENT TEXT:\n"
                                                        "Name: Samir"),
                                                        system_prompt = "CV system prompt")

def test_extract_invoice():
    llm_client = Mock()
    prompt_manager = Mock()

    prompt_manager.get_system_prompt.return_value = "Invoice system prompt"
    prompt_manager.get_extraction_prompt.return_value = "Extract Invoice details"
    llm_client.generate.return_value = '{"invoice_number": "INV001"}'
    extractor = DocumentExtractor(llm_client, prompt_manager)
    result = extractor.extract(document_type="invoice", document_text="Invoice Number: INV001")
    assert result == '{"invoice_number": "INV001"}'

def test_llm_response_is_returned():
    llm_client = Mock()
    prompt_manager = Mock()

    prompt_manager.get_system_prompt.return_value = "System prompt"
    prompt_manager.get_extraction_prompt.return_value = "Extraction prompt"
    llm_client.generate.return_value = "Extraction completed"
    extractor = DocumentExtractor(llm_client, prompt_manager)
    result = extractor.extract("cv", "Sample CV")
    assert result == "Extraction completed"

def test_extract_structured():
    llm_client = Mock()
    prompt_manager = Mock()

    llm_client.generate.return_value = """
    {
        "full_name": "Samir Kumar Ram",
        "email": "samir@example.com",
        "skills": ["Java", "Python"]
    }
    """
    extractor = DocumentExtractor(llm_client, prompt_manager)
    result = extractor.extract_structured(document_type = "cv", document_text = "Samir Kumar Ram, Java Developer", response_model = CVData)

    assert isinstance(result, CVData)
    assert result.full_name == "Samir Kumar Ram"
    assert result.email == "samir@example.com"
    assert result.skills == ["Java", "Python"]

def test_extract_structured_invalid_json():
    llm_client = Mock()
    prompt_manager = Mock()

    llm_client.generate.return_value = "This is not a valid JSON"

    extractor = DocumentExtractor(llm_client, prompt_manager)
    with pytest.raises(ValidationError):
        extractor.extract_structured(
            document_type="cv",
            document_text="Sample CV",
            response_model=CVData
        )
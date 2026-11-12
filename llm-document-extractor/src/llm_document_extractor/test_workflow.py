from pathlib import Path
from unittest.mock import Mock
from llm_document_extractor.workflow import CVExtractionWorkflow
from llm_document_extractor.schemas import CVData

def test_workflow_with_string_path():
    document_reader = Mock()
    document_extractor = Mock()
    document_reader.read.return_value = "Sample CV test"
    expected_result = CVData(full_name="Samir Kumar Ram", email="samir@example.com")
    document_extractor.extract_structured.return_value = expected_result
    workflow = CVExtractionWorkflow(document_reader, document_extractor)
    result = workflow.run("resume.pdf")
    document_reader.read.assert_called_once_with("resume.pdf")
    document_extractor.extract_structured.assert_called_once_with(document_type = "cv", document_text = "Sample CV test", response_model = CVData)
    assert result == expected_result

def test_workflow_with_path_object(tmp_path: Path):
    file_path = tmp_path / "resume.pdf"
    document_reader = Mock()
    document_extractor = Mock()
    document_reader.read.return_value = "Sample CV test"
    expected_result = CVData(full_name="Samir Kumar Ram", email="samir@example.com")
    document_extractor.extract_structured.return_value = expected_result
    workflow = CVExtractionWorkflow(document_reader, document_extractor)
    result = workflow.run(file_path)
    document_reader.read.assert_called_once_with(file_path)
    assert result == expected_result
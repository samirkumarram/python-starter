from pathlib import Path
from llm_document_extractor.document_reader import DocumentReader
from llm_document_extractor.document_extractor import DocumentExtractor
from llm_document_extractor.schemas import CVData

class CVExtractionWorkflow:
    def __init__(self, document_reader: DocumentReader, document_extractor: DocumentExtractor):
        self.document_reader = document_reader
        self.document_extractor = document_extractor

    def run(self, file_path: str | Path) -> CVData:
        self.document_text = self.document_reader.read(file_path)
        return self.document_extractor.extract_structured(document_type = "cv", document_text = self.document_text, response_model = CVData)
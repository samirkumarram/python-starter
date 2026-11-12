from pathlib import Path
from docx import Document as DocxDocument
from pypdf import PdfReader

class DocumentReader:
    def read(self, file_path: str | Path) -> str:
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Document not found: {path}")
        if not path.is_file():
            raise ValueError("Provided path is not a file.")
        extension = path.suffix.lower()
        if extension == ".pdf":
            text = self.read_pdf(path)
        elif extension == ".docx":
            text = self.read_docx(path)
        elif extension == ".txt":
            text = path.read_text(encoding="utf-8")
        else:
            raise ValueError(f"Unsupported document format: {extension}")
        if not text.strip():
            raise ValueError("No readable text found in the document.")
        return text.strip()

    def read_pdf(self, path: Path) -> str:
        reader = PdfReader(path)
        pages = [page.extract_text() or "" for page in reader.pages]
        return "\n".join(pages)

    def read_docx(self, path: Path) -> str:
        document = DocxDocument(path)
        paragraphs = [paragraph.text for paragraph in document.paragraphs if paragraph.text.strip()]
        tables = []
        for table in document.tables:
            for row in table.rows:
                row_text = " | ".join(cell.text.strip() for cell in row.cells)
                tables.append(row_text)
        return "\n".join(paragraphs + tables)
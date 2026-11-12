from pathlib import Path
from types import SimpleNamespace

import pytest
from docx import Document

from llm_document_extractor.document_reader import DocumentReader

def test_read_txt(tmp_path: Path):
    file_path = tmp_path / "resume.txt"
    file_path.write_text(
        "Name: Samir\nSkills: Java, Python",
        encoding="utf-8",
    )

    reader = DocumentReader()

    result = reader.read(file_path)

    assert "Name: Samir" in result
    assert "Skills: Java, Python" in result


def test_read_docx(tmp_path: Path):
    file_path = tmp_path / "resume.docx"

    document = Document()
    document.add_paragraph("Name: Samir")
    document.add_paragraph("Skills: Java, Python")

    table = document.add_table(rows=1, cols=2)
    table.cell(0, 0).text = "Experience"
    table.cell(0, 1).text = "5 years"

    document.save(file_path)

    reader = DocumentReader()

    result = reader.read(file_path)

    assert "Name: Samir" in result
    assert "Skills: Java, Python" in result
    assert "Experience" in result
    assert "5 years" in result


def test_read_pdf(tmp_path: Path, monkeypatch):
    file_path = tmp_path / "resume.pdf"
    file_path.touch()

    fake_reader = SimpleNamespace(
        pages=[
            SimpleNamespace(extract_text=lambda: "Name: Samir"),
            SimpleNamespace(extract_text=lambda: "Skills: Java"),
        ]
    )

    monkeypatch.setattr(
        "llm_document_extractor.document_reader.PdfReader",
        lambda path: fake_reader,
    )

    reader = DocumentReader()

    result = reader.read(file_path)

    assert "Name: Samir" in result
    assert "Skills: Java" in result


def test_missing_file():
    reader = DocumentReader()

    with pytest.raises(FileNotFoundError):
        reader.read("missing.pdf")


def test_unsupported_file_type(tmp_path: Path):
    file_path = tmp_path / "resume.xlsx"
    file_path.touch()

    reader = DocumentReader()

    with pytest.raises(ValueError, match="Unsupported document format"):
        reader.read(file_path)


def test_empty_document(tmp_path: Path):
    file_path = tmp_path / "empty.txt"
    file_path.write_text("", encoding="utf-8")

    reader = DocumentReader()

    with pytest.raises(ValueError, match="No readable text"):
        reader.read(file_path)
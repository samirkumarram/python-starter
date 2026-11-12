import pytest
from pydantic import ValidationError

from llm_document_extractor.schemas import (CVData, Education, Experience)

def test_valid_cv_data():
    cv = CVData(
        full_name = "Samir Kumar Ram",
        email = "samir.ram@example.com",
        skills = ["Java", "Python"],
        experience = [
            Experience(
                job_title = "Developer",
                company = "Saksoft",
                start_year = 2021,
                end_year = 2029
            )
        ],
        education = [
            Education(
                degree = "B.Tech",
                graduation_year = 2021
            )
        ]
    )
    assert cv.full_name == "Samir Kumar Ram"
    assert cv.skills == ["Java", "Python"]
    assert len(cv.experience) == 1

def test_optional_fields_can_be_missing():
    cv = CVData(
        full_name = "Samir Kumar Ram",
        email = "samir.ram@gmail.com"
    )

    assert cv.phone is None
    assert cv.location is None
    assert cv.summary is None
    assert cv.skills == []
    assert cv.experience == []
    assert cv.education == []

def test_invalid_full_name_type():
    with pytest.raises(ValidationError):
        CVData(
            full_name = 123,
            email = "samir@gmail.com"
        )

def test_invalid_year_type():
    with pytest.raises(ValidationError):
        Experience(job_title = "Developer", start_year = "two thousnad")
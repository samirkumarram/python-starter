from datetime import date

import pytest
from pydantic import ValidationError

from apiclient.models import Parcel


def test_parcel_accepts_valid_data() -> None:
    parcel = Parcel.model_validate(
        {
            "id": 1,
            "name": "Birch 0001",
            "status": "active",
            "category": "charlie",
            "created": "2026-09-08"
        }
    )
    assert parcel.id == 1
    assert parcel.name == "Birch 0001"
    assert parcel.created.isoformat() == "2026-09-08"


def test_parcel_rejects_invalid_date() -> None:
    with pytest.raises(ValidationError):
        Parcel.model_validate(
            {
                "id": 1,
                "name": "Birch 0001",
                "status": "active",
                "category": "charlie",
                "created": "not-a-date"
            }
        )


def test_parcel_rejects_missing_required_field() -> None:
    with pytest.raises(ValidationError):
        Parcel.model_validate(
            {
                "id": 1,
                "name": "Birch 0001",
                "status": "active",
                "category": "charlie"
            }
        )


def test_parcel_rejects_unexpected_field() -> None:
    with pytest.raises(ValidationError):
        Parcel.model_validate(
            {
                "id": 1,
                "name": "Birch 0001",
                "status": "active",
                "category": "charlie",
                "created": "2026-09-08",
                "unexpected_field": "value"
            }
        )
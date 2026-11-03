from datetime import date

from pydantic import BaseModel, ConfigDict


class Parcel(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id: int
    name: str
    status: str
    category: str
    created: date

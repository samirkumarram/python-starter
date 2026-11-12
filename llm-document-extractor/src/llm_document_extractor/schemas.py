from pydantic import BaseModel, Field

class Experience(BaseModel):
    job_title: str | None = None
    company: str | None = None
    start_year: int | None = None
    end_year: int | None = None

class Education(BaseModel):
    degree: str | None = None
    graduation_year: int | None = None

class CVData(BaseModel):
    full_name: str | None = None
    email: str | None = None
    phone: str | None = None
    location: str | None = None
    summary: str | None = None
    skills: list[str] = Field(default_factory = list)
    experience: list[Experience] = Field(default_factory = list)
    education: list[Education] = Field(default_factory = list)

class InvoiceData(BaseModel):
    invoice_number: str | None = None
    invoice_date: str | None = None
    due_date: str | None = None
    seller_name: str | None = None
    buyer_name: str | None = None
    seller_address: str | None = None
    buyer_address: str | None = None
    total_amount: float | None = None
    tax_amount: float | None = None
    currency: str | None = None
    payment_status: str | None = None

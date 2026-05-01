from pydantic import BaseModel, EmailStr
from typing import Optional, Any
from datetime import datetime

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class OrgUnitOut(BaseModel):
    id: int
    name: str
    type: str
    parent_id: int | None

class UserOut(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    role: str
    org_unit: OrgUnitOut

class AcademicYearCreate(BaseModel):
    name: str
    starts_on: str = ""
    ends_on: str = ""

class TermCreate(BaseModel):
    academic_year_id: int
    name: str
    starts_on: str = ""
    ends_on: str = ""

class SubmissionCreate(BaseModel):
    org_unit_id: int
    term_id: int
    dataset: str
    payload: Any  # dict

class SubmissionOut(BaseModel):
    id: int
    org_unit_id: int
    term_id: int
    dataset: str
    submitted_at: datetime

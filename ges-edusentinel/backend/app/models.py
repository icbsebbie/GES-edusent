from sqlalchemy import String, Integer, ForeignKey, DateTime, Enum, Text, Boolean, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
import enum
from .db import Base

class OrgUnitType(str, enum.Enum):
    HQ = "HQ"
    REGION = "REGION"
    DISTRICT = "DISTRICT"
    CIRCUIT = "CIRCUIT"
    SCHOOL = "SCHOOL"

class Role(str, enum.Enum):
    HQ_ADMIN = "HQ_ADMIN"
    REGION_ADMIN = "REGION_ADMIN"
    DISTRICT_ADMIN = "DISTRICT_ADMIN"
    CIRCUIT_ADMIN = "CIRCUIT_ADMIN"
    SCHOOL_ADMIN = "SCHOOL_ADMIN"
    VIEWER = "VIEWER"

class OrgUnit(Base):
    __tablename__ = "org_units"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), index=True)
    type: Mapped[OrgUnitType] = mapped_column(Enum(OrgUnitType), index=True)
    parent_id: Mapped[int | None] = mapped_column(ForeignKey("org_units.id"), nullable=True, index=True)

    parent = relationship("OrgUnit", remote_side=[id], backref="children")

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    full_name: Mapped[str] = mapped_column(String(255), default="")
    password_hash: Mapped[str] = mapped_column(String(255))
    role: Mapped[Role] = mapped_column(Enum(Role), index=True)
    org_unit_id: Mapped[int] = mapped_column(ForeignKey("org_units.id"), index=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    org_unit = relationship("OrgUnit")

class AcademicYear(Base):
    __tablename__ = "academic_years"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True)  # e.g., 2025/2026
    starts_on: Mapped[str] = mapped_column(String(10), default="")  # ISO date string
    ends_on: Mapped[str] = mapped_column(String(10), default="")

class Term(Base):
    __tablename__ = "terms"
    __table_args__ = (UniqueConstraint("academic_year_id", "name", name="uq_term_year_name"),)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    academic_year_id: Mapped[int] = mapped_column(ForeignKey("academic_years.id"), index=True)
    name: Mapped[str] = mapped_column(String(50))  # Term 1 / Semester 1 etc.
    starts_on: Mapped[str] = mapped_column(String(10), default="")
    ends_on: Mapped[str] = mapped_column(String(10), default="")

    year = relationship("AcademicYear")

class DataSubmission(Base):
    __tablename__ = "data_submissions"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    org_unit_id: Mapped[int] = mapped_column(ForeignKey("org_units.id"), index=True)
    term_id: Mapped[int] = mapped_column(ForeignKey("terms.id"), index=True)
    dataset: Mapped[str] = mapped_column(String(100), index=True)  # e.g., "attendance", "enrolment"
    payload_json: Mapped[str] = mapped_column(Text)  # store JSON as text for MVP
    submitted_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)

    org_unit = relationship("OrgUnit")
    term = relationship("Term")

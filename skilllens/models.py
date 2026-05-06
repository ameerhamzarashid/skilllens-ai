from datetime import datetime

from sqlalchemy import DateTime, Float, Integer, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class JobPosting(Base):
    """
    Clean job posting table.

    Stage 1 keeps skills as comma-separated text.
    Later stages can normalise this into skills and job_skills tables.
    """

    __tablename__ = "job_postings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    job_id: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    title: Mapped[str] = mapped_column(String(255), index=True)
    company: Mapped[str] = mapped_column(String(255), index=True)
    location: Mapped[str] = mapped_column(String(255), index=True)
    country: Mapped[str] = mapped_column(String(100), index=True)

    category: Mapped[str] = mapped_column(String(100), index=True)
    experience_level: Mapped[str] = mapped_column(String(100), index=True)
    work_type: Mapped[str] = mapped_column(String(100), index=True)

    salary_min: Mapped[float | None] = mapped_column(Float, nullable=True)
    salary_max: Mapped[float | None] = mapped_column(Float, nullable=True)
    salary_currency: Mapped[str] = mapped_column(String(20), default="GBP")

    description: Mapped[str] = mapped_column(Text)
    extracted_skills: Mapped[str] = mapped_column(Text)

    posted_date: Mapped[str] = mapped_column(String(50))
    source: Mapped[str] = mapped_column(String(100), default="sample")

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )
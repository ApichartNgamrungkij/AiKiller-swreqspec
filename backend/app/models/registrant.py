from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


# Supports FR-VIEW-02, FR-VIEW-03, FR-VIEW-04, CON-VIEW-01
@dataclass(slots=True)
class RegisteredStudent:
    """A registered student row read from Google Sheets or cached locally."""

    row_id: int | str
    timestamp: datetime | str
    student_id: str
    full_name: str
    faculty: str | None = None
    email: str | None = None

    def __post_init__(self) -> None:
        if not str(self.student_id).strip():
            raise ValueError("student_id is required")
        if not str(self.full_name).strip():
            raise ValueError("full_name is required")

    def to_dict(self) -> dict[str, int | str | None]:
        return {
            "rowId": self.row_id,
            "timestamp": self.timestamp,
            "studentId": self.student_id,
            "fullName": self.full_name,
            "faculty": self.faculty,
            "email": self.email,
        }

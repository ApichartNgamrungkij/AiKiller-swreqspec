from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Protocol


class SheetResponseWriter(Protocol):
    def append_values(
        self,
        spreadsheet_id: str,
        range_name: str,
        values: list[object],
    ) -> dict[str, object]: ...


@dataclass(frozen=True, slots=True)
class GoogleFormSubmission:
    student_id: str
    full_name: str
    submitted_at: datetime


# Supports FR-REG-02, FR-REG-03, IF-GFORM-01, IF-GSHEET-01, ASM-01, ASM-04.
class GoogleFormClient:
    """Submit a simulated Google Form response to its activity sheet."""

    def __init__(self, sheets_client: SheetResponseWriter) -> None:
        self._sheets_client = sheets_client

    def submit(
        self,
        *,
        google_sheet_id: str,
        student_id: str,
        full_name: str,
        range_name: str = "Form Responses 1",
    ) -> GoogleFormSubmission:
        if not student_id.strip():
            raise ValueError("student_id is required")
        if not full_name.strip():
            raise ValueError("full_name is required")

        submitted_at = datetime.now(timezone.utc)
        self._sheets_client.append_values(
            google_sheet_id,
            range_name,
            [submitted_at.isoformat(), student_id.strip(), full_name.strip()],
        )
        return GoogleFormSubmission(
            student_id=student_id.strip(),
            full_name=full_name.strip(),
            submitted_at=submitted_at,
        )

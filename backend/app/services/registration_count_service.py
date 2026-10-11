from __future__ import annotations

from collections.abc import Sequence

from backend.app.integrations.google_sheets_api import GoogleSheetsApi


# Supports FR-REG-04, IF-GSAPI-01, ASM-02, ASM-12.
class RegistrationCountService:
    """Count every saved response without mutating the last successful result."""

    def __init__(self, sheets_api: GoogleSheetsApi) -> None:
        self._sheets_api = sheets_api

    def count_responses(
        self,
        google_sheet_id: str,
        range_name: str = "Form Responses 1",
    ) -> int:
        rows: list[Sequence[object]] = self._sheets_api.read_response_rows(
            google_sheet_id,
            range_name,
        )
        return len(rows)

from __future__ import annotations

from collections.abc import Sequence
from typing import Any


# Supports FR-REG-03, FR-REG-04, IF-GSAPI-01, ASM-02, ASM-12.
class GoogleSheetsApi:
    """Read all response rows from an activity's Google Sheet."""

    def __init__(self, client: Any) -> None:
        self._client = client

    def read_response_rows(
        self,
        google_sheet_id: str,
        range_name: str = "Form Responses 1",
    ) -> list[Sequence[object]]:
        if not google_sheet_id.strip():
            raise ValueError("google_sheet_id is required")
        values = self._client.read_values(google_sheet_id, range_name)
        if not values:
            return []
        if not isinstance(values[0], Sequence) or isinstance(values[0], (str, bytes)):
            raise ValueError("Google Sheets header must be a sequence")

        rows: list[Sequence[object]] = []
        for row in values[1:]:
            if not isinstance(row, Sequence) or isinstance(row, (str, bytes)):
                raise ValueError("Google Sheets response rows must be sequences")
            rows.append(row)
        return rows

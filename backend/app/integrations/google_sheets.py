from __future__ import annotations

import json
import os
from typing import Any

GOOGLE_SHEETS_READONLY_SCOPE = "https://www.googleapis.com/auth/spreadsheets.readonly"


# Supports IF-VIEW-01, FR-VIEW-02, ASM-VIEW-01
class GoogleSheetsClient:
    """Read values from Google Sheets with a Service Account."""

    def __init__(self, service: Any | None = None) -> None:
        self._service = service or self._build_service()

    @staticmethod
    def _build_service() -> Any:
        from google.oauth2 import service_account
        from googleapiclient.discovery import build

        credentials_json = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")
        if not credentials_json:
            raise RuntimeError("GOOGLE_SERVICE_ACCOUNT_JSON is required")

        try:
            credentials_info = json.loads(credentials_json)
        except json.JSONDecodeError as error:
            raise RuntimeError("GOOGLE_SERVICE_ACCOUNT_JSON must contain valid JSON") from error

        credentials = service_account.Credentials.from_service_account_info(
            credentials_info,
            scopes=[GOOGLE_SHEETS_READONLY_SCOPE],
        )
        return build("sheets", "v4", credentials=credentials, cache_discovery=False)

    def read_values(self, spreadsheet_id: str, range_name: str) -> list[list[str]]:
        """Read a range from one activity's Google Sheet."""
        if not spreadsheet_id.strip():
            raise ValueError("spreadsheet_id is required")
        if not range_name.strip():
            raise ValueError("range_name is required")

        response = (
            self._service.spreadsheets()
            .values()
            .get(spreadsheetId=spreadsheet_id, range=range_name)
            .execute()
        )
        values = response.get("values", [])
        if not isinstance(values, list):
            raise ValueError("Google Sheets response values must be a list")
        return values

    # Supports FR-SRCH-01 and IF status polling constraint.
    def read_registration_count(self, spreadsheet_id: str, range_name: str) -> int:
        """Return the number of registration rows, excluding the header row."""
        values = self.read_values(spreadsheet_id, range_name)
        return max(0, len(values) - 1)

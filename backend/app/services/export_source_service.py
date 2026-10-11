from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from urllib.parse import urlparse

from backend.app.integrations.google_sheets import GoogleSheetsClient
from backend.app.models.activity_export_source import ActivityExportSource


@dataclass(frozen=True, slots=True)
class ExportAccessSnapshot:
    """Expose the latest successful source read for one activity."""

    activity_id: int
    response_count: int
    google_sheet_url: str
    last_successful_read_at: datetime

    @property
    def can_export(self) -> bool:
        return self.response_count >= 1


# Supports FR-EXP-01, FR-EXP-02, IF-GSHEET-01, CON-EXPORT-01, ASM-01, ASM-05, ASM-06.
class ExportSourceService:
    """Read registration rows and retain the latest successful source state."""

    def __init__(
        self,
        google_sheets: GoogleSheetsClient,
        sources: dict[int, ActivityExportSource] | None = None,
    ) -> None:
        self._google_sheets = google_sheets
        self._sources = sources if sources is not None else {}

    def read_latest(
        self,
        activity_id: int,
        *,
        spreadsheet_id: str,
        range_name: str = "Form Responses 1",
    ) -> ExportAccessSnapshot:
        source = self._sources.get(activity_id)
        if source is None:
            raise LookupError(f"Export source for activity {activity_id} was not found")
        parsed_url = urlparse(source.google_sheet_url.strip())
        if parsed_url.scheme not in {"http", "https"} or not parsed_url.netloc:
            raise ValueError("Google Sheets URL is not configured")

        response_count = self._google_sheets.read_export_response_count(
            spreadsheet_id,
            range_name,
        )
        read_at = datetime.now(timezone.utc)
        source.last_successful_response_count = response_count
        source.last_successful_read_at = read_at
        return ExportAccessSnapshot(
            activity_id=activity_id,
            response_count=response_count,
            google_sheet_url=source.google_sheet_url,
            last_successful_read_at=read_at,
        )

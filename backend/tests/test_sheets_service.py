from __future__ import annotations

from unittest.mock import Mock

import pytest

from backend.app.integrations.google_sheets import GoogleSheetsClient
from backend.app.services.sheets_service import SheetsService


# Supports IF-VIEW-01, FR-VIEW-02, ASM-VIEW-01
def test_sheets_service_reads_and_maps_registered_students() -> None:
    client = Mock()
    client.read_values.return_value = [
        ["Timestamp", "Student ID", "Full Name", "Faculty", "Email"],
        ["2026-10-10T08:30:00Z", "660510001", "นายสมชาย ใจดี", "วิศวกรรมศาสตร์", "student@example.com"],
    ]

    result = SheetsService(client).fetch_registrants("sheet-001", "Form Responses 1!A:E")

    assert result[0].to_dict() == {
        "rowId": "2",
        "timestamp": "2026-10-10T08:30:00Z",
        "studentId": "660510001",
        "fullName": "นายสมชาย ใจดี",
        "faculty": "วิศวกรรมศาสตร์",
        "email": "student@example.com",
    }
    client.read_values.assert_called_once_with("sheet-001", "Form Responses 1!A:E")


# Supports IF-VIEW-01, FR-VIEW-02
def test_google_sheets_client_reads_values_from_v4_api() -> None:
    service = Mock()
    service.spreadsheets.return_value.values.return_value.get.return_value.execute.return_value = {
        "values": [["Timestamp", "Student ID", "Full Name"]]
    }

    result = GoogleSheetsClient(service).read_values("sheet-001", "A:C")

    assert result == [["Timestamp", "Student ID", "Full Name"]]
    service.spreadsheets.return_value.values.return_value.get.assert_called_once_with(
        spreadsheetId="sheet-001",
        range="A:C",
    )


# Supports IF-VIEW-01, FR-VIEW-02
def test_sheets_service_rejects_rows_without_required_headers() -> None:
    client = Mock()
    client.read_values.return_value = [["Timestamp", "Email"], ["2026-10-10T08:30:00Z", "a@example.com"]]

    with pytest.raises(ValueError, match="missing headers"):
        SheetsService(client).fetch_registrants("sheet-001", "A:B")

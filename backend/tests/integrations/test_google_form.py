from unittest.mock import Mock

from backend.app.integrations.google_form import GoogleFormClient
from backend.app.integrations.google_sheets import GoogleSheetsClient


# Supports AC-REG-02 and IF-GSHEET-01.
def test_AC_REG_02_google_form_response_is_saved() -> None:
    sheets_client = Mock()
    sheets_client.append_values.return_value = {
        "updates": {"updatedRows": 1},
    }
    form_client = GoogleFormClient(sheets_client)

    submission = form_client.submit(
        google_sheet_id="sheet-activity-1",
        student_id="660510001",
        full_name="นายสมชาย ใจดี",
    )

    assert submission.student_id == "660510001"
    sheets_client.append_values.assert_called_once()
    assert sheets_client.append_values.call_args.args[0] == "sheet-activity-1"


def test_google_sheets_client_appends_form_response() -> None:
    service = Mock()
    service.spreadsheets().values().append().execute.return_value = {
        "updates": {"updatedRows": 1},
    }
    client = GoogleSheetsClient(service)

    response = client.append_values(
        "sheet-activity-1",
        "Form Responses 1",
        ["2026-10-11T12:00:00+00:00", "660510001", "นายสมชาย ใจดี"],
    )

    assert response["updates"] == {"updatedRows": 1}

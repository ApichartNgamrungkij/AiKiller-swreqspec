from fastapi import FastAPI
from fastapi.testclient import TestClient

from backend.app.api.google_sheet import (
    get_activity,
    get_current_user,
    get_export_source,
    router,
)
from backend.app.models.activity import Activity
from backend.app.models.activity_export_source import ActivityExportSource


def _client() -> TestClient:
    app = FastAPI()
    app.include_router(router)
    activity = Activity(id=7, owner_id="organizer-1", title="กิจกรรมทดสอบ")
    source = ActivityExportSource(
        activity_id=7,
        google_sheet_url="https://docs.google.com/spreadsheets/d/sheet-7/edit",
    )
    app.dependency_overrides[get_activity] = lambda activity_id: activity
    app.dependency_overrides[get_current_user] = lambda: {
        "user_id": "student-1",
        "role": "student",
    }
    app.dependency_overrides[get_export_source] = lambda activity_id: source
    return TestClient(app)


# Supports AC-EXP-07, ACC-GSHEET-02, NFR-SEC-01.
def test_AC_EXP_07_student_cannot_access_google_sheet() -> None:
    response = _client().get("/activities/7/google-sheet")

    assert response.status_code == 403
    assert "googleSheetUrl" not in response.json()
    assert "sheet-7" not in response.text


# Supports AC-EXP-08, ACC-GSHEET-02, NFR-SEC-02.
def test_AC_EXP_08_student_receives_no_google_sheet_data() -> None:
    response = _client().get("/activities/7/google-sheet")

    assert response.status_code == 403
    assert "values" not in response.text

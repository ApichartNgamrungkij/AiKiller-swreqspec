from fastapi import FastAPI
from fastapi.testclient import TestClient

from backend.app.api.google_sheet_access import (
    get_activity,
    get_current_user,
    router,
)
from backend.app.models.activity import Activity


def _client(user: dict[str, object]) -> TestClient:
    app = FastAPI()
    app.include_router(router)
    activity = Activity(
        id=7,
        title="กิจกรรมทดสอบ",
        owner_id="organizer-1",
        google_sheet_id="sheet-7",
    )
    app.dependency_overrides[get_current_user] = lambda: user
    app.dependency_overrides[get_activity] = lambda activity_id: activity
    return TestClient(app)


# Supports AC-REG-06, ACC-GSHEET-01, NFR-SEC-01.
def test_AC_REG_06_allows_admin_or_activity_organizer_sheet_access() -> None:
    admin_response = _client({"user_id": "admin-1", "role": "admin"}).get(
        "/activities/7/google-sheet-access"
    )
    organizer_response = _client({"user_id": "organizer-1", "role": "organizer"}).get(
        "/activities/7/google-sheet-access"
    )

    assert admin_response.status_code == 200
    assert admin_response.json() == {"activityId": 7, "canAccess": True}
    assert organizer_response.status_code == 200
    assert organizer_response.json() == {"activityId": 7, "canAccess": True}


# Supports AC-REG-06, ACC-GSHEET-02, NFR-SEC-02.
def test_AC_REG_06_denies_student_and_other_organizer_sheet_access() -> None:
    student_response = _client({"user_id": "student-1", "role": "student"}).get(
        "/activities/7/google-sheet-access"
    )
    other_organizer_response = _client(
        {"user_id": "organizer-2", "role": "organizer"}
    ).get("/activities/7/google-sheet-access")

    assert student_response.status_code == 403
    assert other_organizer_response.status_code == 403


# Supports AC-REG-07, ACC-GSHEET-02, NFR-SEC-02.
def test_AC_REG_07_denies_student_direct_sheet_access_without_exposing_sheet_data() -> None:
    response = _client({"user_id": "student-1", "role": "student"}).get(
        "/activities/7/google-sheet-access"
    )

    assert response.status_code == 403
    assert "sheet-7" not in response.text
    assert "values" not in response.text

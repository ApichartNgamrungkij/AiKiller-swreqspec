from __future__ import annotations

from datetime import datetime, timezone

from fastapi import FastAPI
from fastapi.testclient import TestClient

from backend.app.api.deps import verify_event_owner_or_admin
from backend.app.api.registrants import (
    get_activity,
    get_current_user,
    get_registration_cache,
    router,
)
from backend.app.models.activity import Activity
from backend.app.models.registrant import RegisteredStudent
from backend.app.models.registration_summary import ActivityRegistrationSummary, SyncStatus
from backend.app.services.cache_service import RegistrationCache


def _client(user: dict[str, object], summary: ActivityRegistrationSummary | None) -> TestClient:
    app = FastAPI()
    app.include_router(router)
    cache = RegistrationCache()
    if summary is not None:
        cache.save(summary)
    app.dependency_overrides[get_current_user] = lambda: user
    app.dependency_overrides[get_activity] = lambda: Activity(
        id=1,
        title="กิจกรรมทดสอบ",
        owner_id="organizer-1",
    )
    app.dependency_overrides[get_registration_cache] = lambda: cache
    return TestClient(app)


def _summary(status: SyncStatus = SyncStatus.SUCCESS) -> ActivityRegistrationSummary:
    student = RegisteredStudent(
        row_id=2,
        timestamp=datetime(2026, 10, 10, 8, 30, tzinfo=timezone.utc),
        student_id="660510001",
        full_name="นายสมชาย ใจดี",
        faculty="วิศวกรรมศาสตร์",
        email="student@example.com",
    )
    return ActivityRegistrationSummary(
        activity_id=1,
        total_registered=1,
        last_synced_at=student.timestamp,
        sync_status=status,
        cached_responses=[student],
    )


# Supports AC-VIEW-01
def test_AC_VIEW_01_fetch_registrants_success() -> None:
    response = _client({"user_id": "organizer-1", "role": "organizer"}, _summary()).get(
        "/api/v1/activities/1/registrants"
    )

    assert response.status_code == 200
    assert response.json()["totalRegistered"] == 1
    assert response.json()["data"][0]["studentId"] == "660510001"
    assert response.json()["isCache"] is False


# Supports AC-VIEW-03
def test_AC_VIEW_03_fallback_to_cache_on_api_failure() -> None:
    response = _client(
        {"user_id": "organizer-1", "role": "organizer"},
        _summary(SyncStatus.FAILED),
    ).get("/api/v1/activities/1/registrants")

    assert response.status_code == 200
    assert response.json()["syncStatus"] == "FAILED"
    assert response.json()["isCache"] is True
    assert response.json()["lastSyncedAt"] is not None


# Supports AC-VIEW-04
def test_AC_VIEW_04_student_access_forbidden() -> None:
    response = _client({"user_id": "student-1", "role": "student"}, _summary()).get(
        "/api/v1/activities/1/registrants"
    )

    assert response.status_code == 403


# Supports AC-VIEW-05
def test_AC_VIEW_05_authorized_user_access_granted() -> None:
    response = _client({"user_id": "admin-1", "role": "admin"}, _summary()).get(
        "/api/v1/activities/1/registrants"
    )

    assert response.status_code == 200


def test_empty_registration_response_is_successful() -> None:
    response = _client({"user_id": "admin-1", "role": "admin"}, None).get(
        "/api/v1/activities/1/registrants"
    )

    assert response.status_code == 200
    assert response.json()["totalRegistered"] == 0
    assert response.json()["data"] == []

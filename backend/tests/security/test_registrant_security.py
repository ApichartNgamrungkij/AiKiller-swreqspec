from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI
from fastapi.testclient import TestClient

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


REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
HTTPS_CONFIG = REPOSITORY_ROOT / "deployment" / "https-config.yml"


def _client(user: dict[str, object]) -> TestClient:
    app = FastAPI()
    app.include_router(router)

    student = RegisteredStudent(
        row_id=1,
        timestamp="2026-10-10T08:30:00+00:00",
        student_id="660510001",
        full_name="นายสมชาย ใจดี",
        faculty="วิศวกรรมศาสตร์",
        email="student@example.com",
    )
    cache = RegistrationCache()
    cache.save(
        ActivityRegistrationSummary(
            activity_id=1,
            total_registered=1,
            last_synced_at=student.timestamp,
            sync_status=SyncStatus.SUCCESS,
            cached_responses=[student],
        )
    )
    app.dependency_overrides[get_current_user] = lambda: user
    app.dependency_overrides[get_activity] = lambda: Activity(
        id=1,
        title="กิจกรรมทดสอบ",
        owner_id="organizer-1",
    )
    app.dependency_overrides[get_registration_cache] = lambda: cache
    return TestClient(app)


# Supports NFR-SEC-01.
def test_NFR_SEC_01_https_deployment_contract_requires_tls() -> None:
    config = HTTPS_CONFIG.read_text(encoding="utf-8")

    assert "enabled: true" in config
    assert "redirect_http_to_https: true" in config
    assert 'minimum_version: "TLSv1.2"' in config
    assert "hsts:" in config
    assert "enabled: true" in config


# Supports NFR-SEC-02, ACC-VIEW-02.
def test_NFR_SEC_02_student_cannot_receive_registrant_personal_data() -> None:
    response = _client({"user_id": "student-1", "role": "student"}).get(
        "/api/v1/activities/1/registrants"
    )

    assert response.status_code == 403
    assert "660510001" not in response.text
    assert "นายสมชาย ใจดี" not in response.text
    assert "student@example.com" not in response.text


# Supports NFR-SEC-02, ACC-VIEW-01.
def test_NFR_SEC_02_authorized_owner_can_receive_registrants() -> None:
    response = _client({"user_id": "organizer-1", "role": "organizer"}).get(
        "/api/v1/activities/1/registrants"
    )

    assert response.status_code == 200
    assert response.json()["data"][0]["studentId"] == "660510001"

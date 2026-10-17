from fastapi import FastAPI
from fastapi.testclient import TestClient

from backend.app.api.admin_activity_routes import (
    get_activity,
    get_audit_log_store,
    get_current_user,
    router,
)
from backend.app.models.activity import Activity, ActivityStatus
from backend.app.models.activity_audit_log import ActivityAuditLog


def make_client(role="admin", status_value=ActivityStatus.PUBLISHED):
    app = FastAPI()
    app.include_router(router)

    activity = Activity(id=7, title="Test activity", status=status_value)
    logs: list[ActivityAuditLog] = []

    app.dependency_overrides[get_current_user] = lambda: {
        "user_id": 10,
        "role": role,
    }
    app.dependency_overrides[get_activity] = lambda: activity
    app.dependency_overrides[get_audit_log_store] = lambda: logs

    return TestClient(app, base_url="https://testserver"), activity, logs


def test_admin_can_suspend_activity_and_record_audit_log():
    client, activity, logs = make_client()

    response = client.post(
        "/api/v1/admin/activities/7/action",
        headers={"x-forwarded-proto": "https"},
        json={
            "action": "suspend",
            "reason": "ผิดเงื่อนไข",
            "confirmed": True,
        },
    )

    assert response.status_code == 200
    assert response.json()["status"] == ActivityStatus.HIDDEN.value
    assert response.json()["auditLogRecorded"] is True
    assert activity.status == ActivityStatus.HIDDEN
    assert len(logs) == 1
    assert logs[0].reason == "ผิดเงื่อนไข"


def test_non_admin_cannot_change_activity():
    client, activity, logs = make_client(role="student")

    response = client.post(
        "/api/v1/admin/activities/7/action",
        headers={"x-forwarded-proto": "https"},
        json={"action": "delete", "reason": "เหตุผล", "confirmed": True},
    )

    assert response.status_code == 403
    assert activity.status == ActivityStatus.PUBLISHED
    assert logs == []


def test_confirmation_is_required():
    client, activity, logs = make_client()

    response = client.post(
        "/api/v1/admin/activities/7/action",
        headers={"x-forwarded-proto": "https"},
        json={"action": "delete", "reason": "เหตุผล", "confirmed": False},
    )

    assert response.status_code == 400
    assert activity.status == ActivityStatus.PUBLISHED
    assert logs == []


def test_blank_reason_is_rejected():
    client, activity, logs = make_client()

    response = client.post(
        "/api/v1/admin/activities/7/action",
        headers={"x-forwarded-proto": "https"},
        json={"action": "delete", "reason": "   ", "confirmed": True},
    )

    assert response.status_code == 422
    assert activity.status == ActivityStatus.PUBLISHED
    assert logs == []


def test_non_published_activity_cannot_be_changed():
    client, activity, logs = make_client(status_value=ActivityStatus.HIDDEN)

    response = client.post(
        "/api/v1/admin/activities/7/action",
        headers={"x-forwarded-proto": "https"},
        json={"action": "delete", "reason": "เหตุผล", "confirmed": True},
    )

    assert response.status_code == 422
    assert activity.status == ActivityStatus.HIDDEN
    assert logs == []

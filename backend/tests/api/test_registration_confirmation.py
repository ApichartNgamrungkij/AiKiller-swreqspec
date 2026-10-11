from fastapi import FastAPI
from fastapi.testclient import TestClient

from backend.app.api.registration_confirmation import (
    get_notification_service,
    router,
)
from backend.app.services.notification_service import NotificationService


def _client() -> tuple[TestClient, NotificationService]:
    app = FastAPI()
    app.include_router(router)
    service = NotificationService()
    app.dependency_overrides[get_notification_service] = lambda: service
    return TestClient(app), service


# Supports AC-REG-05, FR-REG-07, IF-NOT-01, ASM-10.
def test_AC_REG_05_creates_unread_confirmation_notification() -> None:
    client, service = _client()

    response = client.post(
        "/activities/7/registration-confirmation",
        json={"studentId": "student-1", "message": "ลงทะเบียนกิจกรรมสำเร็จ"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["studentId"] == "student-1"
    assert body["activityId"] == 7
    assert body["message"] == "ลงทะเบียนกิจกรรมสำเร็จ"
    assert body["isRead"] is False
    assert service.list_for_student("student-1")[0].is_read is False


# Supports ASM-10.
def test_notification_is_retained_until_student_reads_it() -> None:
    client, service = _client()
    response = client.post(
        "/activities/7/registration-confirmation",
        json={"studentId": "student-1", "message": "ยืนยันการลงทะเบียน"},
    )
    notification_id = response.json()["notificationId"]

    service.mark_as_read(notification_id, "student-1")

    notifications = service.list_for_student("student-1")
    assert len(notifications) == 1
    assert notifications[0].is_read is True

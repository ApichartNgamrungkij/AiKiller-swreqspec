from __future__ import annotations

from typing import Any, Mapping

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from backend.app.services.notification_service import (
    NotificationService,
    RegistrationNotification,
)


router = APIRouter(prefix="/activities", tags=["registration"])
_notification_service = NotificationService()


class RegistrationConfirmationRequest(BaseModel):
    studentId: str
    message: str


def get_notification_service() -> NotificationService:
    return _notification_service


def _notification_response(notification: RegistrationNotification) -> dict[str, Any]:
    return {
        "notificationId": notification.notification_id,
        "studentId": notification.student_id,
        "activityId": notification.activity_id,
        "message": notification.message,
        "isRead": notification.is_read,
        "createdAt": notification.created_at,
    }


# Supports FR-REG-07, IF-NOT-01, ASM-05, ASM-10.
@router.post("/{activity_id}/registration-confirmation")
def create_registration_confirmation(
    activity_id: int,
    payload: RegistrationConfirmationRequest,
    service: NotificationService = Depends(get_notification_service),
) -> dict[str, Any]:
    try:
        notification = service.create_registration_confirmation(
            student_id=payload.studentId,
            activity_id=activity_id,
            message=payload.message,
        )
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(error),
        ) from error
    return _notification_response(notification)

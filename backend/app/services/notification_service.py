from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass(slots=True)
class RegistrationNotification:
    notification_id: int
    student_id: str
    activity_id: int
    message: str
    is_read: bool
    created_at: datetime


# Supports FR-REG-07, IF-NOT-01, ASM-05, ASM-10.
class NotificationService:
    """Create and retain in-site registration confirmation notifications."""

    def __init__(self) -> None:
        self._notifications: list[RegistrationNotification] = []
        self._next_id = 1

    def create_registration_confirmation(
        self,
        *,
        student_id: str,
        activity_id: int,
        message: str,
    ) -> RegistrationNotification:
        if not student_id.strip():
            raise ValueError("student_id is required")
        if not message.strip():
            raise ValueError("message is required")

        notification = RegistrationNotification(
            notification_id=self._next_id,
            student_id=student_id.strip(),
            activity_id=activity_id,
            message=message.strip(),
            is_read=False,
            created_at=datetime.now(timezone.utc),
        )
        self._notifications.append(notification)
        self._next_id += 1
        return notification

    def list_for_student(self, student_id: str) -> list[RegistrationNotification]:
        return [
            notification
            for notification in self._notifications
            if notification.student_id == student_id
        ]

    def mark_as_read(self, notification_id: int, student_id: str) -> None:
        for notification in self._notifications:
            if notification.notification_id == notification_id and notification.student_id == student_id:
                notification.is_read = True
                return
        raise KeyError(f"Notification {notification_id} was not found")

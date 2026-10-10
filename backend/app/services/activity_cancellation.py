from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Iterable, Mapping

from backend.app.models.activity import Activity


# Supports FR-ACT-09, ASM-ACT-06
@dataclass(frozen=True)
class ActivityCancellationNotice:
    registration_id: int | None
    user_id: int | None
    message: str


# Supports FR-ACT-09, ASM-ACT-06
class ActivityCancellationService:
    def cancel_activity(
        self,
        activity: Activity,
        *,
        reason: str,
        registrations: Iterable[Mapping[str, Any]] | None = None,
    ) -> Activity:
        if activity is None:
            raise ValueError("activity is required")
        if not reason or not str(reason).strip():
            raise ValueError("reason is required before cancelling an activity")

        activity.status = "cancelled"
        activity.cancelled_at = datetime.now(timezone.utc)
        activity.reason = str(reason).strip()

        notices: list[ActivityCancellationNotice] = []
        for registration in registrations or []:
            notices.append(
                ActivityCancellationNotice(
                    registration_id=registration.get("registration_id"),
                    user_id=registration.get("user_id"),
                    message="กิจกรรมถูกยกเลิกแล้ว",
                )
            )

        activity.notifications = [
            {
                "registration_id": notice.registration_id,
                "user_id": notice.user_id,
                "message": notice.message,
            }
            for notice in notices
        ]
        return activity

    # Supports FR-ACT-09, ASM-ACT-06
    def build_notifications(self, registrations: Iterable[Mapping[str, Any]]) -> list[dict[str, Any]]:
        return [
            {
                "registration_id": registration.get("registration_id"),
                "user_id": registration.get("user_id"),
                "message": "กิจกรรมถูกยกเลิกแล้ว",
            }
            for registration in registrations
        ]

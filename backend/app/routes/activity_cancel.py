from __future__ import annotations

from typing import Any, Mapping

from backend.app.models.activity import Activity
from backend.app.services.activity_cancellation import ActivityCancellationService


# Supports FR-ACT-09, ASM-ACT-06
def cancel_activity_route(
    activity: Activity,
    *,
    reason: str,
    registrations: list[Mapping[str, Any]] | None = None,
) -> dict[str, Any]:
    service = ActivityCancellationService()
    cancelled_activity = service.cancel_activity(
        activity,
        reason=reason,
        registrations=registrations,
    )
    return {
        "activity": cancelled_activity,
        "notifications": list(getattr(cancelled_activity, "notifications", [])),
        "cancelled": True,
    }

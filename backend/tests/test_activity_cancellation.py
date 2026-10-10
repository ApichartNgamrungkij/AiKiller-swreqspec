from __future__ import annotations

import pytest

from backend.app.models.activity import Activity, ActivityStatus
from backend.app.routes.activity_cancel import cancel_activity_route


# Supports AC-ACT-09
def test_AC_ACT_09_activity_cancellation_keeps_status_and_sends_notifications() -> None:
    activity = Activity(
        id=15,
        title="โครงการวันจิตอาสา",
        status=ActivityStatus.PUBLISHED,
    )
    registrations = [
        {"registration_id": 1, "user_id": 101},
        {"registration_id": 2, "user_id": 202},
    ]

    result = cancel_activity_route(
        activity,
        reason="ยกเลิกตามคำสั่งหน่วยงาน",
        registrations=registrations,
    )

    assert result["cancelled"] is True
    assert result["activity"].status == "cancelled"
    assert result["activity"].cancelled_at is not None
    assert [entry["user_id"] for entry in result["notifications"]] == [101, 202]
    assert all("ยกเลิก" in entry["message"] for entry in result["notifications"])

    with pytest.raises(ValueError, match="reason is required"):
        cancel_activity_route(activity, reason=" ", registrations=registrations)

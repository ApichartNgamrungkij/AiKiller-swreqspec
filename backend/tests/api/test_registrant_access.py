import pytest
from fastapi import HTTPException

from backend.app.api.deps import verify_event_owner_or_admin
from backend.app.models.activity import Activity


# Supports AC-VIEW-04, ACC-VIEW-02, FR-VIEW-05
def test_AC_VIEW_04_student_access_forbidden() -> None:
    with pytest.raises(HTTPException) as error:
        verify_event_owner_or_admin(
            {"user_id": "student-1", "role": "student"},
            {"owner_id": "organizer-1"},
        )

    assert error.value.status_code == 403


# Supports AC-VIEW-05, ACC-VIEW-01, FR-VIEW-05
def test_AC_VIEW_05_admin_or_activity_owner_access_granted() -> None:
    activity = Activity(id=1, title="กิจกรรมทดสอบ", owner_id="organizer-1")

    verify_event_owner_or_admin({"user_id": "admin-1", "role": "admin"}, activity)
    verify_event_owner_or_admin(
        {"user_id": "organizer-1", "role": "organizer"},
        activity,
    )


# Supports AC-VIEW-04, ACC-VIEW-01, NFR-SEC-02
def test_AC_VIEW_04_other_organizer_access_forbidden() -> None:
    activity = Activity(id=1, title="กิจกรรมทดสอบ", owner_id="organizer-1")

    with pytest.raises(HTTPException) as error:
        verify_event_owner_or_admin(
            {"user_id": "organizer-2", "role": "organizer"},
            activity,
        )

    assert error.value.status_code == 403


def test_AC_VIEW_05_owner_access_accepts_numeric_user_id() -> None:
    activity = Activity(id=1, title="กิจกรรมทดสอบ", owner_id="101")

    verify_event_owner_or_admin({"user_id": 101, "role": "organizer"}, activity)

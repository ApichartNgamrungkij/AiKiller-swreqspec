from __future__ import annotations

from typing import Any, Mapping

from fastapi import HTTPException, status

from backend.app.services.access_control import is_activity_owner, is_admin_user


# Supports ACC-VIEW-01, ACC-VIEW-02, FR-VIEW-05, NFR-SEC-02
def verify_event_owner_or_admin(
    user: Mapping[str, object] | None,
    activity: Mapping[str, object] | Any,
) -> None:
    """Allow only an admin or the activity owner to view registrants."""

    if is_admin_user(user):
        return

    if is_activity_owner(user, activity):
        return

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="ไม่มีสิทธิ์ดูข้อมูลผู้ลงทะเบียนของกิจกรรมนี้",
    )

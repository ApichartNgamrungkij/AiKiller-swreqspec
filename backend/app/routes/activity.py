from __future__ import annotations

from typing import Any, Mapping


class ActivityCreatorAccessError(PermissionError):
    """Raised when an unauthorized user tries to open or use the activity-create flow."""


# Supports CON-ACT-01, FR-ACT-01, DOM-ACT-03
def is_authorized_activity_creator(user: Mapping[str, Any] | None) -> bool:
    if not user:
        return False

    role = str(user.get("role", "")).strip().lower()
    if role in {"admin", "administrator", "organizer", "activity_manager"}:
        return True

    if isinstance(user.get("is_organizer"), bool):
        return user["is_organizer"]

    if isinstance(user.get("can_create_activity"), bool):
        return user["can_create_activity"]

    if isinstance(user.get("approved_by_admin"), bool):
        return user["approved_by_admin"]

    if isinstance(user.get("is_admin"), bool):
        return user["is_admin"]

    return False


# Supports CON-ACT-01, FR-ACT-01, DOM-ACT-03
def require_activity_creator_access(user: Mapping[str, Any] | None) -> None:
    if not is_authorized_activity_creator(user):
        raise ActivityCreatorAccessError(
            'เฉพาะผู้จัดกิจกรรมที่ได้รับสิทธิ์จาก Admin เท่านั้นที่สามารถเปิดหน้า “สร้างกิจกรรมใหม่” ได้'
        )

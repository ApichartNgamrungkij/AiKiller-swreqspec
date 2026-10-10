from __future__ import annotations

from typing import Any, Mapping

from backend.app.models.activity import Activity
from backend.app.services.activity_service import activity_to_student_view, create_activity, published_activity_list
from backend.app.services.activity_visibility_service import student_activity_list


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


# Supports FR-ACT-05, FR-ACT-06, FR-ACT-07, DOM-ACT-03
def create_activity_route(
    user: Mapping[str, Any] | None,
    payload: Mapping[str, Any],
    *,
    store: list[Activity] | None = None,
    next_id: int = 1,
) -> Activity:
    require_activity_creator_access(user)
    return create_activity(payload, store=store, next_id=next_id)


# Supports FR-ACT-05, FR-ACT-06, FR-ACT-07, DOM-ACT-03
def submit_activity_creation(
    user: Mapping[str, Any] | None,
    payload: Mapping[str, Any],
    *,
    store: list[Activity] | None = None,
    next_id: int = 1,
) -> dict[str, Any]:
    activity = create_activity_route(user, payload, store=store, next_id=next_id)
    visible_activities = [activity_to_student_view(item) for item in student_activity_list(published_activity_list(store or [activity]))]
    return {
        "activity": activity_to_student_view(activity),
        "visible_activities": visible_activities,
        "published_count": len(visible_activities),
    }


create_activity_for_user = create_activity_route

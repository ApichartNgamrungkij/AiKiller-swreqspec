from __future__ import annotations

from typing import Any, Iterable, Mapping

from backend.app.models.activity import Activity, ActivityCategory, ActivityStatus
from backend.app.services.activity_validation import validate_activity_submission


# Supports FR-ACT-05, FR-ACT-06, FR-ACT-07, DOM-ACT-03
def create_activity(
    payload: Mapping[str, Any],
    *,
    store: list[Activity] | None = None,
    next_id: int = 1,
) -> Activity:
    normalized_payload = dict(payload)
    errors = validate_activity_submission(normalized_payload)
    if errors:
        raise ValueError("; ".join(errors))

    if store is not None:
        activity_id = max((activity.id for activity in store if activity.id is not None), default=0) + 1
    else:
        activity_id = next_id

    category_name = ActivityCategory.normalize(normalized_payload.get("category"))
    activity = Activity(
        id=activity_id,
        title=str(normalized_payload.get("title") or "").strip(),
        status=ActivityStatus.PUBLISHED,
        category=category_name.value,
        venue=str(normalized_payload.get("venue") or "").strip(),
        max_participants=int(normalized_payload.get("max_participants") or 0),
        volunteer_hours=int(normalized_payload.get("volunteer_hours") or 0),
        registration_url=str(normalized_payload.get("registration_url") or "").strip(),
    )
    activity.slots = list(normalized_payload.get("slots") or [])

    if store is not None:
        store.append(activity)

    return activity


# Supports FR-ACT-06, DOM-ACT-03
def published_activity_list(activities: Iterable[Activity]) -> list[Activity]:
    return [activity for activity in activities if activity.status == ActivityStatus.PUBLISHED]


# Supports FR-ACT-05, FR-ACT-06, DOM-ACT-03
def activity_to_student_view(activity: Activity) -> dict[str, Any]:
    return {
        "id": activity.id,
        "title": activity.title,
        "category": activity.category,
        "venue": activity.venue,
        "status": activity.status.value,
        "visible_to_students": activity.is_visible_to_students,
        "registration_url": activity.registration_url,
        "slots": getattr(activity, "slots", []),
    }


# Supports FR-SRCH-01, FR-SRCH-02, FR-SRCH-03, DOM — กรองกิจกรรมตามบทบาทและประเภทก่อนส่งกลับให้ผู้ใช้
def filter_activities_for_role(
    activities: Iterable[Activity],
    *,
    user: Mapping[str, Any] | None = None,
    category: str | None = None,
) -> list[Activity]:
    visible = [item for item in activities if item.status == ActivityStatus.PUBLISHED]
    if category is not None:
        normalized_category = ActivityCategory.normalize(category).value
        visible = [item for item in visible if item.category == normalized_category]

    role = str((user or {}).get("role", "")).strip().lower()
    if role in {"student", "", None}:
        return visible
    if role in {"admin", "administrator", "organizer", "activity_manager"}:
        return list(visible)
    return visible


# Supports FR-SRCH-01, FR-SRCH-05, IF — คืนรายละเอียดกิจกรรมตาม id สำหรับใช้แสดงในหน้าดูข้อมูลแบบเห็นภาพก่อนส่งต่อไป Google Form
def find_activity_by_id(activities: Iterable[Activity], activity_id: Any) -> Activity | None:
    for item in activities:
        if item.id == activity_id:
            return item
    return None


# Supports FR-SRCH-01, FR-SRCH-03
def student_search_results(
    activities: Iterable[Activity],
    *,
    category: str | None = None,
    user: Mapping[str, Any] | None = None,
) -> list[dict[str, Any]]:
    return [
        activity_to_student_view(item)
        for item in filter_activities_for_role(activities, user=user, category=category)
    ]

from __future__ import annotations

from collections.abc import Iterable, Mapping
from typing import Any

from backend.app.models.activity import Activity, ActivityCategory, ActivityStatus
from backend.app.services.activity_service import (
    activity_to_student_view,
    filter_activities_for_role,
    find_activity_by_id,
    published_activity_list,
)


# Supports FR-SRCH-01, FR-SRCH-03, DOM — รายการกิจกรรมสำหรับนักศึกษาต้องแสดงเฉพาะกิจกรรมที่ถูกเปิดเผยและยังมีที่ว่าง
def list_activities(
    *,
    activities: Iterable[Activity] | None = None,
    user: Mapping[str, Any] | None = None,
    category: str | None = None,
) -> list[dict[str, Any]]:
    base_activities = list(activities or [])
    filtered = filter_activities_for_role(
        base_activities,
        user=user,
        category=category,
    )
    return [activity_to_student_view(item) for item in filtered]


# Supports FR-SRCH-01, FR-SRCH-05, IF — รายละเอียดกิจกรรมต้องคืนข้อมูลที่ใช้แสดงก่อนตัดสินใจลงทะเบียนต่อ
def get_activity_detail(
    activity_id: int,
    *,
    activities: Iterable[Activity] | None = None,
) -> dict[str, Any] | None:
    activity = find_activity_by_id(activities or [], activity_id)
    if activity is None:
        return None
    return activity_to_student_view(activity)


# Supports FR-SRCH-02, FR-SRCH-03, DOM — ระบุประเภทประกอบการกรองตามที่มหาวิทยาลัยรับรองเท่านั้น
def search_activities(
    *,
    activities: Iterable[Activity] | None = None,
    user: Mapping[str, Any] | None = None,
    category: str | None = None,
) -> list[dict[str, Any]]:
    if category is not None:
        category_value = ActivityCategory.normalize(category).value
        return [
            activity_to_student_view(item)
            for item in filter_activities_for_role(activities or [], user=user, category=category_value)
        ]
    return list_activities(activities=activities, user=user, category=category)


student_visible_activities = list_activities

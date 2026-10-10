from __future__ import annotations

from collections.abc import Iterable

from backend.app.models.activity import Activity, ActivityStatus


# Supports FR-DEL-05, IF-HIDE-01, ASM-02, ASM-03
def is_activity_visible_to_students(activity: Activity) -> bool:
    return activity.status == ActivityStatus.PUBLISHED


# Supports FR-DEL-05, IF-HIDE-01, ASM-02, ASM-03
def student_activity_list(activities: Iterable[Activity]) -> list[Activity]:
    return [activity for activity in activities if is_activity_visible_to_students(activity)]

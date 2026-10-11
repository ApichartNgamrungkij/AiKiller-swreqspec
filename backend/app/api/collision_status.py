from __future__ import annotations

from datetime import datetime
from typing import Any, Mapping, Sequence

from backend.app.models.personal_busy_period import PersonalBusyPeriod
from backend.app.services.collision_service import get_collision_status


# Supports FR-SRCH-02, FR-SRCH-03, IF — returns a warning while leaving detail access available.
def collision_status(
    activity_id: int | str,
    activity_start: datetime,
    activity_end: datetime,
    *,
    student_schedule: Sequence[PersonalBusyPeriod | Mapping[str, Any]],
) -> dict[str, object]:
    return get_collision_status(activity_id, activity_start, activity_end, student_schedule)

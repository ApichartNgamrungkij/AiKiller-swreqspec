from __future__ import annotations

from datetime import datetime
from typing import Any, Mapping, Sequence

from backend.app.models.personal_busy_period import PersonalBusyPeriod
from backend.app.services.overlap_checker import check_schedule_overlap


# Supports FR-SRCH-02, FR-SRCH-03, IF — reports collisions without removing the activity from results.
def get_collision_status(
    activity_id: int | str,
    activity_start: datetime,
    activity_end: datetime,
    schedule: Sequence[PersonalBusyPeriod | Mapping[str, Any]],
) -> dict[str, object]:
    periods = [
        item if isinstance(item, PersonalBusyPeriod) else PersonalBusyPeriod.from_dict(dict(item))
        for item in schedule
    ]
    result = check_schedule_overlap(activity_start, activity_end, periods)
    overlapping_periods = result["overlapping_periods"]
    return {
        "activity_id": activity_id,
        "has_collision": result["has_overlap"],
        "warning": result["message"],
        "severity": "red" if result["has_overlap"] else None,
        "overlapping_periods": [
            period.to_dict() for period in overlapping_periods  # type: ignore[union-attr]
        ],
    }

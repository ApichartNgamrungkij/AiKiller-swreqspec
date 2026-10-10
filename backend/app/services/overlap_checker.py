from __future__ import annotations

from datetime import date, datetime
from typing import Iterable, Sequence

from backend.app.models.personal_busy_period import PersonalBusyPeriod


# Supports FR-SCHED-02, FR-SCHED-04, FR-SCHED-05, IF-SCHED-01, ASM-SCHED-02, ASM-SCHED-06
def date_range_inclusive(start_date: date, end_date: date) -> list[date]:
    if end_date < start_date:
        raise ValueError("end_date must be on or after start_date")

    current = start_date
    dates: list[date] = []
    while current <= end_date:
        dates.append(current)
        current = current.fromordinal(current.toordinal() + 1)
    return dates


# Supports FR-SCHED-02, FR-SCHED-05, ASM-SCHED-02, ASM-SCHED-06
def time_intervals_overlap(start_a: datetime, end_a: datetime, start_b: datetime, end_b: datetime) -> bool:
    """Treat intervals as half-open [start, end), so 09:00-10:00 and 10:00-11:00 do not overlap."""
    return start_a < end_b and start_b < end_a


# Supports FR-SCHED-04, FR-SCHED-05, AC-SCHED-05, AC-SCHED-07
def find_overlapping_busy_periods(
    activity_start: datetime,
    activity_end: datetime,
    busy_periods: Sequence[PersonalBusyPeriod],
) -> list[PersonalBusyPeriod]:
    if activity_end <= activity_start:
        return []

    overlaps: list[PersonalBusyPeriod] = []
    for period in busy_periods:
        if period.overlaps_with_activity(activity_start, activity_end):
            overlaps.append(period)
    return overlaps


# Supports FR-SCHED-04, FR-SCHED-05, AC-SCHED-05, AC-SCHED-07
def check_schedule_overlap(
    activity_start: datetime,
    activity_end: datetime,
    busy_periods: Sequence[PersonalBusyPeriod],
) -> dict[str, object]:
    overlaps = find_overlapping_busy_periods(activity_start, activity_end, busy_periods)
    has_overlap = bool(overlaps)
    message = (
        "มีช่วงเวลาคาบเกี่ยวกับตารางส่วนตัวของคุณ" if has_overlap else "ไม่มีช่วงเวลาคาบเกี่ยวกับตารางส่วนตัวของคุณ"
    )
    return {
        "has_overlap": has_overlap,
        "message": message,
        "overlapping_periods": overlaps,
        "activity_start": activity_start,
        "activity_end": activity_end,
    }


def overlaps_with_busy_periods(
    activity_start: datetime,
    activity_end: datetime,
    busy_periods: Sequence[PersonalBusyPeriod],
) -> bool:
    return bool(find_overlapping_busy_periods(activity_start, activity_end, busy_periods))

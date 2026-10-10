from __future__ import annotations

from datetime import date, datetime, time

from backend.app.models.personal_busy_period import PersonalBusyPeriod
from backend.app.services.overlap_checker import (
    check_schedule_overlap,
    find_overlapping_busy_periods,
    time_intervals_overlap,
)


# Supports AC-SCHED-02, AC-SCHED-04, AC-SCHED-05, AC-SCHED-07
def test_AC_SCHED_02_daily_repeat_and_exclusive_end() -> None:
    period = PersonalBusyPeriod(
        id=1,
        student_id=101,
        start_date="2026-01-05",
        end_date="2026-01-07",
        start_time="09:00:00",
        end_time="10:00:00",
    )

    activity_start = datetime(2026, 1, 6, 9, 30)
    activity_end = datetime(2026, 1, 6, 10, 30)
    assert period.overlaps_with_activity(activity_start, activity_end) is True

    boundary_start = datetime(2026, 1, 6, 10, 0)
    boundary_end = datetime(2026, 1, 6, 11, 0)
    assert period.overlaps_with_activity(boundary_start, boundary_end) is False

    assert time_intervals_overlap(
        datetime(2026, 1, 6, 9, 0),
        datetime(2026, 1, 6, 10, 0),
        datetime(2026, 1, 6, 10, 0),
        datetime(2026, 1, 6, 11, 0),
    ) is False


# Supports AC-SCHED-04, AC-SCHED-05
def test_AC_SCHED_05_overlap_shows_warning() -> None:
    saved_periods = [
        PersonalBusyPeriod(
            id=7,
            student_id=101,
            start_date=date(2026, 1, 2),
            end_date=date(2026, 1, 8),
            start_time=time(14, 0),
            end_time=time(16, 0),
        )
    ]

    activity_start = datetime(2026, 1, 5, 15, 30)
    activity_end = datetime(2026, 1, 5, 16, 30)

    overlap = check_schedule_overlap(activity_start, activity_end, saved_periods)
    assert overlap["has_overlap"] is True
    assert "มีช่วงเวลาคาบเกี่ยว" in overlap["message"]
    assert find_overlapping_busy_periods(activity_start, activity_end, saved_periods) == saved_periods


# Supports AC-SCHED-04
def test_AC_SCHED_04_saved_period_reusable_for_later_activity_check() -> None:
    saved_period = PersonalBusyPeriod(
        id=9,
        student_id=101,
        start_date="2026-03-01",
        end_date="2026-03-10",
        start_time="08:30",
        end_time="09:30",
    )

    later_activity_start = datetime(2026, 3, 4, 8, 45)
    later_activity_end = datetime(2026, 3, 4, 9, 15)

    assert saved_period.overlaps_with_activity(later_activity_start, later_activity_end) is True
    assert check_schedule_overlap(later_activity_start, later_activity_end, [saved_period])["has_overlap"] is True

from __future__ import annotations

from datetime import date, datetime, time

from backend.app.models.personal_busy_period import PersonalBusyPeriod
from backend.app.routes.me_schedule import create_busy_period, get_my_schedule, update_busy_period
from backend.app.services.overlap_checker import check_schedule_overlap


# Supports AC-SCHED-02, AC-SCHED-03, AC-SCHED-04
def test_AC_SCHED_02_create_or_update_busy_period() -> None:
    student = {"student_id": "S-100", "is_authenticated": True}
    store: list[PersonalBusyPeriod] = [
        PersonalBusyPeriod(
            id=1,
            student_id="S-100",
            start_date=date(2026, 1, 5),
            end_date=date(2026, 1, 10),
            start_time=time(9, 0),
            end_time=time(10, 0),
        ),
        PersonalBusyPeriod(
            id=2,
            student_id="S-100",
            start_date=date(2026, 1, 5),
            end_date=date(2026, 1, 10),
            start_time=time(14, 0),
            end_time=time(15, 0),
        ),
    ]

    updated = update_busy_period(
        student,
        1,
        {
            "id": 1,
            "student_id": "S-100",
            "start_date": "2026-01-06",
            "end_date": "2026-01-12",
            "start_time": "11:00",
            "end_time": "12:00",
        },
        store=store,
    )

    assert len(updated["schedule"]) == 2
    assert [entry["id"] for entry in updated["schedule"]] == [1, 2]
    assert updated["schedule"][0]["start_time"] == "11:00:00"
    assert updated["schedule"][0]["end_time"] == "12:00:00"


# Supports AC-SCHED-03
def test_AC_SCHED_03_add_period_preserves_existing() -> None:
    student = {"student_id": "S-200", "is_authenticated": True}
    store = [
        PersonalBusyPeriod(
            id=10,
            student_id="S-200",
            start_date=date(2026, 2, 1),
            end_date=date(2026, 2, 3),
            start_time=time(8, 0),
            end_time=time(9, 0),
        )
    ]

    created = create_busy_period(
        student,
        {
            "id": 11,
            "student_id": "S-200",
            "start_date": "2026-02-05",
            "end_date": "2026-02-07",
            "start_time": "13:00",
            "end_time": "14:00",
        },
        store=store,
    )

    assert len(created["schedule"]) == 2
    assert created["schedule"][0]["id"] == 10
    assert created["schedule"][1]["id"] == 11


# Supports AC-SCHED-04
def test_AC_SCHED_04_saved_period_reusable() -> None:
    student = {"student_id": "S-300", "is_authenticated": True}
    store = [
        PersonalBusyPeriod(
            id=100,
            student_id="S-300",
            start_date=date(2026, 3, 1),
            end_date=date(2026, 3, 7),
            start_time=time(10, 0),
            end_time=time(11, 0),
        )
    ]

    saved = get_my_schedule(student, store=store)
    assert saved["schedule"][0]["student_id"] == "S-300"

    overlap_result = check_schedule_overlap(
        datetime(2026, 3, 4, 10, 30),
        datetime(2026, 3, 4, 11, 30),
        [PersonalBusyPeriod.from_dict(saved["schedule"][0])],
    )
    assert overlap_result["has_overlap"] is True

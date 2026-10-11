from datetime import datetime

from backend.app.api.collision_status import collision_status


# Supports AC-SRCH-03
def test_AC_SRCH_03_overlap_returns_red_warning_without_removing_activity() -> None:
    result = collision_status(
        1,
        datetime(2026, 11, 7, 9, 30),
        datetime(2026, 11, 7, 10, 30),
        student_schedule=[
            {
                "id": 7,
                "student_id": "S-001",
                "start_date": "2026-11-07",
                "end_date": "2026-11-07",
                "start_time": "09:00",
                "end_time": "10:00",
            }
        ],
    )

    assert result["activity_id"] == 1
    assert result["has_collision"] is True
    assert result["severity"] == "red"
    assert result["overlapping_periods"]

from __future__ import annotations

from backend.app.services.activity_validation import (
    is_valid_activity_submission,
    normalize_activity_category,
    validate_activity_submission,
)


# Supports AC-ACT-04
def test_AC_ACT_04_missing_required_fields_are_reported() -> None:
    errors = validate_activity_submission({"title": "กิจกรรม", "category": "วิชาการ"})

    assert any("กรุณากรอกข้อมูล venue" in message for message in errors)
    assert any("กรุณากรอกข้อมูล max_participants" in message for message in errors)
    assert any("กรุณากรอกข้อมูล volunteer_hours" in message for message in errors)


# Supports AC-ACT-05
def test_AC_ACT_05_valid_category_and_required_fields_are_accepted() -> None:
    payload = {
        "title": "กิจกรรมบำเพ็ญประโยชน์",
        "category": "บำเพ็ญประโยชน์",
        "venue": "ศูนย์บริการชุมชน",
        "max_participants": 30,
        "volunteer_hours": 5,
        "registration_url": "https://example.com/register",
        "slots": [
            {"slot_date": "2026-04-15", "start_time": "09:00", "end_time": "12:00"},
            {"slot_date": "2026-04-15", "start_time": "13:00", "end_time": "16:00"},
        ],
    }

    assert normalize_activity_category("บำเพ็ญประโยชน์") == "บำเพ็ญประโยชน์"
    assert validate_activity_submission(payload) == []
    assert is_valid_activity_submission(payload) is True


# Supports AC-ACT-07
def test_AC_ACT_07_no_new_approval_step_is_added_to_workflow() -> None:
    invalid = {
        "title": "กิจกรรมตรวจสอบ",
        "category": "กีฬา",
        "venue": "สนามกีฬา",
        "max_participants": 40,
        "volunteer_hours": 2,
        "approval_required": True,
    }

    errors = validate_activity_submission(invalid)
    assert any("ระบบไม่เพิ่มขั้นตอนอนุมัติใหม่เข้ามาใน workflow" in error for error in errors)
    assert is_valid_activity_submission(invalid) is False

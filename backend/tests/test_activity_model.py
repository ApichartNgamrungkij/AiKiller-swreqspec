from __future__ import annotations

from datetime import date

import pytest

from backend.app.models.activity import ActivityCategory, ActivityDraft
from backend.app.models.activity_slot import ActivitySlot


# Supports AC-ACT-02
def test_AC_ACT_02_activity_accepts_required_fields_and_multi_slot_schedule() -> None:
    draft = ActivityDraft(
        title="โครงการวันจิตอาสา",
        category=ActivityCategory.ACADEMIC,
        venue="หอประชุมใหญ่",
        max_participants=120,
        volunteer_hours=8,
        registration_url="https://example.com/register",
        slots=[
            ActivitySlot(slot_date="2026-02-12", start_time="09:00", end_time="12:00", label="เช้า"),
            ActivitySlot(slot_date="2026-02-12", start_time="13:00", end_time="16:00", label="บ่าย"),
        ],
    )

    assert draft.category == ActivityCategory.ACADEMIC
    assert len(draft.slots) == 2
    assert draft.slots[0].slot_date == date(2026, 2, 12)
    assert draft.slots[1].label == "บ่าย"
    assert draft.to_dict()["registration_url"] == "https://example.com/register"


# Supports AC-ACT-05
def test_AC_ACT_05_valid_category_and_required_fields_are_enforced() -> None:
    valid = ActivityDraft.from_dict(
        {
            "title": "กิจกรรมประชุมวิชาการ",
            "category": "วิชาการ",
            "venue": "อาคารเรียนรวม",
            "max_participants": 80,
            "volunteer_hours": 4,
            "registration_url": "https://example.com/academic",
            "slots": [{
                "slot_date": "2026-03-04",
                "start_time": "08:30",
                "end_time": "10:30",
                "label": "เช้า",
            }],
        }
    )
    assert valid.category == ActivityCategory.ACADEMIC

    with pytest.raises(ValueError, match="Unsupported activity category"):
        ActivityDraft(
            title="กิจกรรมไม่ผ่าน",
            category="ไม่เป็นประเภทที่มหาวิทยาลัยรับรอง",
            venue="ห้องเรียน",
            max_participants=10,
            volunteer_hours=1,
            slots=[
                ActivitySlot(slot_date="2026-03-05", start_time="9:00", end_time="10:00"),
            ],
        )

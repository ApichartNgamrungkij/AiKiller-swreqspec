from __future__ import annotations

import pytest

from backend.app.models.activity import ActivityStatus
from backend.app.routes.activity import ActivityCreatorAccessError, create_activity_route, submit_activity_creation
from backend.app.services.activity_service import create_activity, published_activity_list
from backend.app.services.activity_visibility_service import student_activity_list


# Supports AC-ACT-05, AC-ACT-06
def test_AC_ACT_05_and_AC_ACT_06_valid_activity_is_saved_and_visible_to_students() -> None:
    store: list = []
    payload = {
        "title": "โครงการจิตอาสาเชิงรุก",
        "category": "บำเพ็ญประโยชน์",
        "venue": "หอประชุมมหาวิทยาลัย",
        "max_participants": 45,
        "volunteer_hours": 6,
        "registration_url": "https://example.com/register/humanity",
        "slots": [
            {"slot_date": "2026-05-20", "start_time": "09:00", "end_time": "12:00", "label": "เช้า"},
            {"slot_date": "2026-05-20", "start_time": "13:00", "end_time": "16:00", "label": "บ่าย"},
        ],
    }

    activity = create_activity(payload, store=store)
    published = published_activity_list(store)
    visible = student_activity_list(published)

    assert activity.status == ActivityStatus.PUBLISHED
    assert activity.id == 1
    assert [item.id for item in visible] == [1]
    assert visible[0].title == "โครงการจิตอาสาเชิงรุก"


# Supports AC-ACT-05, AC-ACT-07
def test_AC_ACT_05_and_AC_ACT_07_system_rejects_new_approval_workflow_steps() -> None:
    invalid = {
        "title": "โครงการไล่ล่าระดับแผนก",
        "category": "กีฬา",
        "venue": "สนามกีฬากลาง",
        "max_participants": 50,
        "volunteer_hours": 4,
        "approval_required": True,
        "slots": [{"slot_date": "2026-06-12", "start_time": "08:30", "end_time": "10:30"}],
    }

    with pytest.raises(ValueError, match="ระบบไม่เพิ่มขั้นตอนอนุมัติใหม่เข้ามาใน workflow"):
        create_activity(invalid)


# Supports AC-ACT-01, AC-ACT-05
def test_AC_ACT_01_and_AC_ACT_05_only_authenticated_organizers_can_submit_new_activity() -> None:
    store: list = []

    with pytest.raises(ActivityCreatorAccessError, match="ได้รับสิทธิ์จาก Admin"):
        create_activity_route({}, {"title": "xx", "category": "วิชาการ"}, store=store)

    result = submit_activity_creation(
        {"role": "organizer"},
        {
            "title": "กิจกรรมฝึกอบรม",
            "category": "วิชาการ",
            "venue": "ห้องปฏิบัติการ",
            "max_participants": 30,
            "volunteer_hours": 2,
            "registration_url": "https://example.com/learn",
            "slots": [{"slot_date": "2026-07-04", "start_time": "09:00", "end_time": "11:00"}],
        },
        store=store,
    )

    assert result["activity"]["title"] == "กิจกรรมฝึกอบรม"
    assert result["published_count"] == 1

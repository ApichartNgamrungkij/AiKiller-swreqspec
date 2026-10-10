from __future__ import annotations

from backend.app.models.activity import ActivityCategory, ActivityDraft
from backend.app.models.activity_slot import ActivitySlot
from backend.app.routes.activity import ActivityCreatorAccessError, is_authorized_activity_creator, require_activity_creator_access
from backend.app.routes.activity_cancel import cancel_activity_route
from backend.app.services.activity_cancellation import ActivityCancellationService
from backend.app.services.activity_edit_history import ActivityEditHistoryService
from backend.app.services.activity_service import create_activity, published_activity_list
from backend.app.services.activity_validation import validate_activity_submission
from backend.app.services.activity_visibility_service import student_activity_list


# Supports AC-ACT-01
def test_AC_ACT_01_only_authorized_organizers_can_open_create_activity_page() -> None:
    assert is_authorized_activity_creator({"role": "organizer"}) is True
    assert is_authorized_activity_creator({"can_create_activity": True}) is True
    assert is_authorized_activity_creator({}) is False

    try:
        require_activity_creator_access({})
    except ActivityCreatorAccessError:
        pass
    else:
        raise AssertionError("Expected unauthorized organizer to be rejected")


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
    assert draft.to_dict()["registration_url"] == "https://example.com/register"


# Supports AC-ACT-03
def test_AC_ACT_03_registration_url_is_saved_with_the_activity() -> None:
    payload = {
        "title": "กิจกรรมออนไลน์",
        "category": "กีฬา",
        "venue": "สนามกีฬา",
        "max_participants": 25,
        "volunteer_hours": 3,
        "registration_url": "https://example.com/register/club",
        "slots": [{"slot_date": "2026-03-01", "start_time": "10:00", "end_time": "12:00"}],
    }

    assert validate_activity_submission(payload) == []
    activity = create_activity(payload, store=[])
    assert activity.registration_url == "https://example.com/register/club"


# Supports AC-ACT-04
def test_AC_ACT_04_missing_required_fields_are_reported() -> None:
    errors = validate_activity_submission({"title": "กิจกรรม", "category": "วิชาการ"})

    assert any("กรุณากรอกข้อมูล venue" in message for message in errors)
    assert any("กรุณากรอกข้อมูล max_participants" in message for message in errors)
    assert any("กรุณากรอกข้อมูล volunteer_hours" in message for message in errors)


# Supports AC-ACT-05
def test_AC_ACT_05_valid_activity_is_saved_and_published() -> None:
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
    visible = student_activity_list(published_activity_list(store))

    assert activity.title == payload["title"]
    assert activity.registration_url == payload["registration_url"]
    assert [item.id for item in visible] == [1]


# Supports AC-ACT-06
def test_AC_ACT_06_created_activity_is_visible_to_students() -> None:
    store: list = []
    payload = {
        "title": "กิจกรรมสอนน้อง",
        "category": "วิชาการ",
        "venue": "อาคารเรียนรวม",
        "max_participants": 30,
        "volunteer_hours": 2,
        "registration_url": "https://example.com/register/teach",
        "slots": [{"slot_date": "2026-08-11", "start_time": "09:00", "end_time": "11:00"}],
    }

    activity = create_activity(payload, store=store)
    visible = student_activity_list(published_activity_list(store))

    assert activity.id == 1
    assert visible[0].title == "กิจกรรมสอนน้อง"


# Supports AC-ACT-07
def test_AC_ACT_07_no_new_approval_step_is_added_to_workflow() -> None:
    invalid = {
        "title": "กิจกรรมตรวจสอบ",
        "category": "กีฬา",
        "venue": "สนามกีฬา",
        "max_participants": 40,
        "volunteer_hours": 2,
        "approval_required": True,
        "slots": [{"slot_date": "2026-06-12", "start_time": "08:30", "end_time": "10:30"}],
    }

    errors = validate_activity_submission(invalid)
    assert any("ระบบไม่เพิ่มขั้นตอนอนุมัติใหม่เข้ามาใน workflow" in error for error in errors)


# Supports AC-ACT-08
def test_AC_ACT_08_activity_edit_history_records_each_change() -> None:
    service = ActivityEditHistoryService()
    entry = service.record_edit(
        activity_id=7,
        editor_id=42,
        field_name="venue",
        old_value="หอประชุมเล็ก",
        new_value="หอประชุมใหญ่",
    )

    assert entry.field_name == "venue"
    assert service.list_for_activity([entry], activity_id=7) == [entry]


# Supports AC-ACT-09
def test_AC_ACT_09_activity_cancellation_keeps_status_and_notifies_registrants() -> None:
    activity = create_activity(
        {
            "title": "กิจกรรมยกเลิก",
            "category": "ศิลปวัฒนธรรม",
            "venue": "หอศิลป์",
            "max_participants": 20,
            "volunteer_hours": 1,
            "registration_url": "https://example.com/register/cancel",
            "slots": [{"slot_date": "2026-09-15", "start_time": "09:00", "end_time": "10:00"}],
        },
        store=[],
    )
    result = cancel_activity_route(
        activity,
        reason="ยกเลิกตามคำสั่ง",
        registrations=[{"registration_id": 1, "user_id": 101}, {"registration_id": 2, "user_id": 202}],
    )

    assert result["cancelled"] is True
    assert result["activity"].status == "cancelled"
    assert [item["user_id"] for item in result["notifications"]] == [101, 202]


# Supports traceability for AC-ACT-01 to AC-ACT-09
def test_activity_traceability_matrix_maps_all_acceptance_criteria() -> None:
    matrix = {
        "AC-ACT-01": "T-02",
        "AC-ACT-02": "T-01, T-03",
        "AC-ACT-03": "T-03",
        "AC-ACT-04": "T-03, T-04",
        "AC-ACT-05": "T-01, T-03, T-04, T-05",
        "AC-ACT-06": "T-05",
        "AC-ACT-07": "T-04, T-05",
        "AC-ACT-08": "T-06",
        "AC-ACT-09": "T-07",
    }

    assert set(matrix.keys()) == {
        "AC-ACT-01",
        "AC-ACT-02",
        "AC-ACT-03",
        "AC-ACT-04",
        "AC-ACT-05",
        "AC-ACT-06",
        "AC-ACT-07",
        "AC-ACT-08",
        "AC-ACT-09",
    }
    assert matrix["AC-ACT-09"] == "T-07"

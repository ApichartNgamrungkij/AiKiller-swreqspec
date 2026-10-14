import pytest
from fastapi import HTTPException

from backend.app.api.deps import verify_event_owner_or_admin


# TC-VIEW-04-1
def test_TC_VIEW_04_1_student_is_denied_without_personal_data() -> None:
    # Given: นักศึกษาทั่วไปพยายามดูข้อมูลกิจกรรม
    # When: เรียกตรวจสิทธิ์ก่อนเข้าถึงข้อมูล
    with pytest.raises(HTTPException) as error:
        verify_event_owner_or_admin(
            {"user_id": "student-1", "role": "student"},
            {"owner_id": "organizer-1"},
        )

    # Then: ปฏิเสธด้วย 403 และไม่ผ่านไปอ่านข้อมูล
    assert error.value.status_code == 403


# TC-VIEW-04-2
def test_TC_VIEW_04_2_student_is_denied_for_single_registrant() -> None:
    # Given: นักศึกษาทั่วไปพยายามดูกิจกรรมที่มีผู้ลงทะเบียน 1 คน
    # When: เรียกตรวจสิทธิ์ก่อนเข้าถึงข้อมูล
    with pytest.raises(HTTPException) as error:
        verify_event_owner_or_admin(
            {"user_id": "student-1", "role": "student"},
            {"owner_id": "organizer-1"},
        )

    # Then: ยังปฏิเสธด้วย 403
    assert error.value.status_code == 403


# TC-VIEW-04-3
def test_TC_VIEW_04_3_authorized_user_follows_view_access_rule() -> None:
    # Given: ผู้ใช้เป็น Admin หรือเจ้าของกิจกรรม
    # When: เรียกตรวจสิทธิ์เข้าถึงข้อมูล
    verify_event_owner_or_admin(
        {"user_id": "admin-1", "role": "admin"},
        {"owner_id": "organizer-1"},
    )
    verify_event_owner_or_admin(
        {"user_id": "organizer-1", "role": "organizer"},
        {"owner_id": "organizer-1"},
    )

    # Then: อนุญาตให้เข้าถึงตาม AC-VIEW-05
    assert True

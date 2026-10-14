import pytest
from fastapi import HTTPException

from backend.app.api.deps import verify_event_owner_or_admin


# TC-VIEW-05-1
def test_TC_VIEW_05_1_admin_can_view_registrants() -> None:
    # Given: ผู้ใช้เป็น Admin
    # When: ตรวจสิทธิ์เข้าถึงข้อมูลผู้ลงทะเบียน
    verify_event_owner_or_admin(
        {"user_id": "admin-1", "role": "admin"},
        {"owner_id": "organizer-1"},
    )

    # Then: ระบบอนุญาตให้เข้าถึง
    assert True


# TC-VIEW-05-2
def test_TC_VIEW_05_2_owner_can_view_single_registrant() -> None:
    # Given: ผู้ใช้เป็นเจ้าของกิจกรรมที่มีผู้ลงทะเบียน 1 คน
    # When: ตรวจสิทธิ์เข้าถึงข้อมูลผู้ลงทะเบียน
    verify_event_owner_or_admin(
        {"user_id": "organizer-1", "role": "organizer"},
        {"owner_id": "organizer-1"},
    )

    # Then: ระบบอนุญาตให้เข้าถึง
    assert True


# TC-VIEW-05-3
def test_TC_VIEW_05_3_non_owner_organizer_is_denied() -> None:
    # Given: ผู้จัดกิจกรรมไม่ใช่เจ้าของและไม่ใช่ Admin
    # When: พยายามตรวจสิทธิ์เข้าถึงข้อมูล
    with pytest.raises(HTTPException) as error:
        verify_event_owner_or_admin(
            {"user_id": "organizer-2", "role": "organizer"},
            {"owner_id": "organizer-1"},
        )

    # Then: ปฏิเสธด้วย 403 Forbidden
    assert error.value.status_code == 403

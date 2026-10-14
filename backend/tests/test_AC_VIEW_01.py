from backend.tests.api.test_registrants import _client, _summary
from backend.app.models.registrant import RegisteredStudent


# TC-VIEW-01-1
def test_TC_VIEW_01_1_owner_sees_registrant_count_and_names() -> None:
    # Given: กิจกรรมของผู้จัดมีผู้ลงทะเบียนอย่างน้อย 2 คนและดึงข้อมูลสำเร็จ
    summary = _summary()
    summary.cached_responses = [
        summary.cached_responses[0],
        RegisteredStudent(
            row_id=3,
            timestamp=summary.cached_responses[0].timestamp,
            student_id="660510002",
            full_name="นางสาวสมหญิง รักเรียน",
            faculty="วิทยาศาสตร์",
            email="student2@example.com",
        ),
    ]
    summary.total_registered = 2

    # When: ผู้จัดเปิดข้อมูลผู้ลงทะเบียนของกิจกรรมตนเอง
    response = _client(
        {"user_id": "organizer-1", "role": "organizer"},
        summary,
    ).get("/api/v1/activities/1/registrants")

    # Then: จำนวนและรายชื่อตรงกับข้อมูลจาก Google Sheets
    body = response.json()
    assert response.status_code == 200
    assert body["totalRegistered"] == 2
    assert [item["studentId"] for item in body["data"]] == [
        "660510001",
        "660510002",
    ]


# TC-VIEW-01-2
def test_TC_VIEW_01_2_owner_sees_single_registrant() -> None:
    # Given: กิจกรรมของผู้จัดมีผู้ลงทะเบียนพอดี 1 คนและดึงข้อมูลสำเร็จ
    # When: ผู้จัดเปิดข้อมูลผู้ลงทะเบียนของกิจกรรมตนเอง
    response = _client(
        {"user_id": "organizer-1", "role": "organizer"},
        _summary(),
    ).get("/api/v1/activities/1/registrants")

    # Then: แสดงจำนวน 1 และรายชื่อผู้ลงทะเบียนคนนั้น
    body = response.json()
    assert response.status_code == 200
    assert body["totalRegistered"] == 1
    assert body["data"][0]["studentId"] == "660510001"
    assert body["data"][0]["fullName"] == "นายสมชาย ใจดี"


# TC-VIEW-01-3
def test_TC_VIEW_01_3_owner_sees_empty_state_without_registrants() -> None:
    # Given: กิจกรรมของผู้จัดยังไม่มีผู้ลงทะเบียน
    # When: ผู้จัดเปิดข้อมูลผู้ลงทะเบียนของกิจกรรมตนเอง
    response = _client(
        {"user_id": "organizer-1", "role": "organizer"},
        None,
    ).get("/api/v1/activities/1/registrants")

    # Then: API คืน 200, totalRegistered 0 และ data ว่างตาม CON-VIEW-01
    body = response.json()
    assert response.status_code == 200
    assert body["totalRegistered"] == 0
    assert body["data"] == []

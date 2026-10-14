from unittest.mock import Mock

from backend.app.jobs.polling_worker import RegistrationPollingWorker
from backend.app.models.registrant import RegisteredStudent
from backend.app.services.cache_service import RegistrationCache


def _student(student_id: str, full_name: str) -> RegisteredStudent:
    return RegisteredStudent(
        row_id=student_id,
        timestamp="2026-10-10T08:30:00Z",
        student_id=student_id,
        full_name=full_name,
    )


# TC-VIEW-02-1
def test_TC_VIEW_02_1_count_updates_after_new_registration() -> None:
    # Given: มีผู้ลงทะเบียนใหม่และข้อมูลถูกบันทึกใน Google Sheets แล้ว
    sheets_service = Mock()
    sheets_service.fetch_registrants.side_effect = [
        [_student("660510001", "นายสมชาย ใจดี")],
        [
            _student("660510001", "นายสมชาย ใจดี"),
            _student("660510002", "นางสาวสมหญิง รักเรียน"),
        ],
    ]
    worker = RegistrationPollingWorker(
        sheets_service,
        RegistrationCache(),
        poll_interval_seconds=60,
    )

    # When: ระบบทำ Polling รอบถัดไปภายใน 2 นาที
    first = worker.poll_activity("ACT-001", "sheet-001", "A:E")
    second = worker.poll_activity("ACT-001", "sheet-001", "A:E")

    # Then: จำนวนผู้ลงทะเบียนใหม่ถูกอัปเดต
    assert first is not None
    assert second is not None
    assert second.total_registered == 2
    assert len(second.cached_responses) == 2


# TC-VIEW-02-2
def test_TC_VIEW_02_2_count_updates_at_two_minute_boundary() -> None:
    # Given: มีผู้ลงทะเบียนใหม่และข้อมูลถูกบันทึกใน Google Sheets แล้ว
    sheets_service = Mock()
    sheets_service.fetch_registrants.return_value = [
        _student("660510001", "นายสมชาย ใจดี"),
        _student("660510002", "นางสาวสมหญิง รักเรียน"),
    ]
    worker = RegistrationPollingWorker(
        sheets_service,
        RegistrationCache(),
        poll_interval_seconds=120,
    )

    # When: ระบบทำ Polling ที่ขอบเขตเวลา 2 นาที
    result = worker.poll_activity("ACT-001", "sheet-001", "A:E")

    # Then: ระบบรองรับช่วงเวลาไม่เกิน 2 นาทีและแสดงจำนวนใหม่
    assert result is not None
    assert worker._poll_interval_seconds == 120
    assert result.total_registered == 2

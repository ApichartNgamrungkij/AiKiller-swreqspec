from unittest.mock import Mock

from backend.app.jobs.polling_worker import RegistrationPollingWorker
from backend.app.models.registrant import RegisteredStudent
from backend.app.models.registration_summary import SyncStatus
from backend.app.services.cache_service import RegistrationCache


def _student(student_id: str = "660510001") -> RegisteredStudent:
    return RegisteredStudent(
        row_id=1,
        timestamp="2026-10-10T08:30:00Z",
        student_id=student_id,
        full_name="นายสมชาย ใจดี",
    )


# TC-VIEW-03-1
def test_TC_VIEW_03_1_cached_registrants_show_when_sheets_api_fails() -> None:
    # Given: Google Sheets API ล้มเหลวและมีข้อมูลล่าสุดใน Cache
    sheets_service = Mock()
    sheets_service.fetch_registrants.return_value = [_student()]
    cache = RegistrationCache()
    worker = RegistrationPollingWorker(sheets_service, cache)
    successful = worker.poll_activity("ACT-001", "sheet-001", "A:E")
    sheets_service.fetch_registrants.side_effect = OSError("API down")

    # When: ผู้จัดกิจกรรมเข้าดูข้อมูลผู้ลงทะเบียน
    result = worker.poll_activity("ACT-001", "sheet-001", "A:E")

    # Then: คืนข้อมูลล่าสุดจาก Cache พร้อมสถานะล้มเหลวและเวลาเดิม
    assert successful is not None
    assert result is not None
    assert result.sync_status is SyncStatus.FAILED
    assert result.cached_responses[0].student_id == "660510001"
    assert result.last_synced_at == successful.last_synced_at


# TC-VIEW-03-2
def test_TC_VIEW_03_2_cached_single_registrant_shows_with_last_sync_time() -> None:
    # Given: API ล้มเหลวและ Cache มีผู้ลงทะเบียน 1 คน
    sheets_service = Mock()
    sheets_service.fetch_registrants.return_value = [_student()]
    cache = RegistrationCache()
    worker = RegistrationPollingWorker(sheets_service, cache)
    worker.poll_activity("ACT-001", "sheet-001", "A:E")
    sheets_service.fetch_registrants.side_effect = OSError("API down")

    # When: ผู้จัดกิจกรรมเข้าดูข้อมูลผู้ลงทะเบียน
    result = worker.poll_activity("ACT-001", "sheet-001", "A:E")

    # Then: ข้อมูลไม่ว่างและมีเวลาอัปเดตล่าสุด
    assert result is not None
    assert result.total_registered == 1
    assert result.last_synced_at is not None

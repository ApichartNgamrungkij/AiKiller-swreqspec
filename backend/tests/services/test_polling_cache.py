from __future__ import annotations

from unittest.mock import Mock

import pytest

from backend.app.models.registrant import RegisteredStudent
from backend.app.models.registration_summary import SyncStatus
from backend.app.services.cache_service import RegistrationCache
from backend.app.jobs.polling_worker import RegistrationPollingWorker


def _student() -> RegisteredStudent:
    return RegisteredStudent(
        row_id=2,
        timestamp="2026-10-10T08:30:00Z",
        student_id="660510001",
        full_name="นายสมชาย ใจดี",
    )


# Supports IF-VIEW-01, FR-VIEW-03, NFR-PERF-01, ASM-VIEW-02
def test_AC_VIEW_02_polling_saves_latest_registration_snapshot() -> None:
    sheets_service = Mock()
    sheets_service.fetch_registrants.return_value = [_student()]
    cache = RegistrationCache()
    worker = RegistrationPollingWorker(
        sheets_service,
        cache,
        poll_interval_seconds=60,
    )

    result = worker.poll_activity("ACT-001", "sheet-001", "A:E")

    assert result is not None
    assert result.sync_status is SyncStatus.SUCCESS
    assert result.total_registered == 1
    assert cache.get("ACT-001") == result
    sheets_service.fetch_registrants.assert_called_once_with("sheet-001", "A:E")


# Supports IF-VIEW-02, FR-VIEW-04
def test_AC_VIEW_03_api_failure_returns_last_cached_snapshot_as_failed() -> None:
    sheets_service = Mock()
    sheets_service.fetch_registrants.return_value = [_student()]
    cache = RegistrationCache()
    worker = RegistrationPollingWorker(sheets_service, cache)
    successful = worker.poll_activity("ACT-001", "sheet-001", "A:E")
    assert successful is not None
    last_synced_at = successful.last_synced_at

    sheets_service.fetch_registrants.side_effect = OSError("Google Sheets unavailable")

    result = worker.poll_activity("ACT-001", "sheet-001", "A:E")

    assert result is not None
    assert result.sync_status is SyncStatus.FAILED
    assert result.total_registered == 1
    assert result.last_synced_at == last_synced_at
    assert result.cached_responses[0].student_id == "660510001"


# Supports IF-VIEW-01, NFR-PERF-01, ASM-VIEW-02
def test_polling_worker_rejects_interval_outside_one_to_two_minutes() -> None:
    with pytest.raises(ValueError, match="between 60 and 120"):
        RegistrationPollingWorker(Mock(), RegistrationCache(), poll_interval_seconds=30)

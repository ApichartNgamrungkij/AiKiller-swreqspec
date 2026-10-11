from unittest.mock import Mock

import pytest

from backend.app.models.activity import RegistrationStatus
from backend.app.services.registration_count_service import RegistrationCountService
from backend.app.services.registration_status_service import RegistrationStatusService


# Supports FR-REG-04, FR-REG-05, NFR-PERF-01, ASM-08.
def test_registration_count_service_does_not_change_data_on_failed_read() -> None:
    sheets_api = Mock()
    sheets_api.read_response_rows.side_effect = RuntimeError("Google Sheets unavailable")
    service = RegistrationCountService(sheets_api)

    with pytest.raises(RuntimeError, match="unavailable"):
        service.count_responses("sheet-1")

    sheets_api.read_response_rows.assert_called_once_with("sheet-1", "Form Responses 1")


# Supports FR-REG-04, FR-REG-05, NFR-PERF-01, ASM-08.
def test_status_sync_keeps_last_successful_snapshot_on_failed_read() -> None:
    sheets_api = Mock()
    sheets_api.read_response_rows.return_value = [["student-1"]]
    count_service = RegistrationCountService(sheets_api)
    status_service = RegistrationStatusService(count_service)

    previous = status_service.sync("activity-1", 2, "sheet-1")
    assert previous.response_count == 1
    assert previous.registration_status is RegistrationStatus.AVAILABLE

    sheets_api.read_response_rows.side_effect = RuntimeError("Google Sheets unavailable")
    with pytest.raises(RuntimeError, match="unavailable"):
        status_service.sync("activity-1", 2, "sheet-1")

    assert status_service.get("activity-1") is previous
    assert status_service.get("activity-1").response_count == 1
    assert status_service.get("activity-1").registration_status is RegistrationStatus.AVAILABLE
    assert status_service.get("activity-1").last_successful_sync_at == previous.last_successful_sync_at

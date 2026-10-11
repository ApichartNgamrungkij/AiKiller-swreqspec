from unittest.mock import Mock

import pytest

from backend.app.integrations.google_sheets import GoogleSheetsClient
from backend.app.jobs.status_polling import ActivityStatusConfig, ActivityStatusPolling
from backend.app.services.activity_status_sync import ActivityStatusSynchronizer


# Supports AC-SRCH-07: a full Google Sheets snapshot changes the activity status.
def test_AC_SRCH_07_full_sheet_snapshot_updates_status_to_full() -> None:
    sheets_client = Mock()
    sheets_client.read_registration_count.return_value = 10
    synchronizer = ActivityStatusSynchronizer(sheets_client)

    snapshot = synchronizer.sync(1, 10, "sheet-1", "A:E")

    assert snapshot.status == "full"
    assert snapshot.booked_slots == 10
    assert synchronizer.get(1) == snapshot


def test_google_sheets_client_counts_rows_without_header() -> None:
    service = Mock()
    service.spreadsheets().values().get().execute.return_value = {
        "values": [["student_id"], ["660510001"], ["660510002"]]
    }

    client = GoogleSheetsClient(service)

    assert client.read_registration_count("sheet-1", "A:A") == 2


def test_status_polling_accepts_one_to_two_minute_interval() -> None:
    polling = ActivityStatusPolling(
        ActivityStatusSynchronizer(Mock()),
        poll_interval_seconds=60,
        scheduler=Mock(),
    )

    assert polling._poll_interval_seconds == 60


def test_status_polling_rejects_interval_outside_constraint() -> None:
    with pytest.raises(ValueError, match="between 60 and 120"):
        ActivityStatusPolling(
            ActivityStatusSynchronizer(Mock()),
            poll_interval_seconds=30,
            scheduler=Mock(),
        )

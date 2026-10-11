from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Protocol


class RegistrationCountReader(Protocol):
    def read_registration_count(self, spreadsheet_id: str, range_name: str) -> int: ...


@dataclass(frozen=True, slots=True)
class ActivityStatusSnapshot:
    activity_id: int | str
    capacity: int
    booked_slots: int
    status: str
    synced_at: datetime


# Supports FR-SRCH-01 and the IF status update within two minutes constraint.
class ActivityStatusSynchronizer:
    """Synchronize an activity badge from the latest Google Sheets count."""

    def __init__(self, sheets_client: RegistrationCountReader) -> None:
        self._sheets_client = sheets_client
        self._snapshots: dict[int | str, ActivityStatusSnapshot] = {}

    def sync(
        self,
        activity_id: int | str,
        capacity: int,
        spreadsheet_id: str,
        range_name: str,
    ) -> ActivityStatusSnapshot:
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        booked_slots = self._sheets_client.read_registration_count(
            spreadsheet_id,
            range_name,
        )
        snapshot = ActivityStatusSnapshot(
            activity_id=activity_id,
            capacity=capacity,
            booked_slots=booked_slots,
            status="full" if booked_slots >= capacity else "open",
            synced_at=datetime.now(timezone.utc),
        )
        self._snapshots[activity_id] = snapshot
        return snapshot

    def get(self, activity_id: int | str) -> ActivityStatusSnapshot | None:
        return self._snapshots.get(activity_id)

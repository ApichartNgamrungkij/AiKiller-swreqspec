from __future__ import annotations

from copy import deepcopy
from threading import RLock

from backend.app.models.registration_summary import (
    ActivityRegistrationSummary,
    SyncStatus,
)


# Supports IF-VIEW-02, FR-VIEW-04
class RegistrationCache:
    """Store the latest registration snapshot for fallback reads."""

    def __init__(self) -> None:
        self._snapshots: dict[int | str, ActivityRegistrationSummary] = {}
        self._lock = RLock()

    def save(self, summary: ActivityRegistrationSummary) -> None:
        with self._lock:
            self._snapshots[summary.activity_id] = deepcopy(summary)

    def get(self, activity_id: int | str) -> ActivityRegistrationSummary | None:
        with self._lock:
            snapshot = self._snapshots.get(activity_id)
            return deepcopy(snapshot) if snapshot is not None else None

    def get_failed(self, activity_id: int | str) -> ActivityRegistrationSummary | None:
        snapshot = self.get(activity_id)
        if snapshot is None:
            return None
        snapshot.sync_status = SyncStatus.FAILED
        return snapshot

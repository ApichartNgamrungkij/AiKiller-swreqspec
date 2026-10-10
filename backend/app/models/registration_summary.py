from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

from backend.app.models.registrant import RegisteredStudent


# Supports FR-VIEW-03, FR-VIEW-04, CON-VIEW-01
class SyncStatus(str, Enum):
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"


# Supports FR-VIEW-01, FR-VIEW-03, FR-VIEW-04, CON-VIEW-01
@dataclass(slots=True)
class ActivityRegistrationSummary:
    """Latest registration count and cached responses for one activity."""

    activity_id: int | str
    total_registered: int
    last_synced_at: datetime | str | None
    sync_status: SyncStatus
    cached_responses: list[RegisteredStudent] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.total_registered < 0:
            raise ValueError("total_registered cannot be negative")
        if not isinstance(self.sync_status, SyncStatus):
            self.sync_status = SyncStatus(self.sync_status)
        if self.total_registered != len(self.cached_responses):
            raise ValueError("total_registered must match cached_responses")

    def to_dict(self) -> dict[str, object]:
        return {
            "activityId": self.activity_id,
            "totalRegistered": self.total_registered,
            "lastSyncedAt": self.last_synced_at,
            "syncStatus": self.sync_status.value,
            "cachedResponses": [
                response.to_dict() for response in self.cached_responses
            ],
        }

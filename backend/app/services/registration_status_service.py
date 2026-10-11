from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone

from backend.app.integrations.google_form_settings import GoogleFormSettings
from backend.app.models.activity import RegistrationStatus
from backend.app.services.registration_count_service import RegistrationCountService


@dataclass(frozen=True, slots=True)
class RegistrationStatusSnapshot:
    """The latest successful registration count and derived activity status."""

    activity_id: int | str
    response_count: int
    capacity: int
    registration_status: RegistrationStatus
    last_successful_sync_at: datetime


# Supports FR-REG-04, FR-REG-05, FR-REG-06, IF-GFORM-02, NFR-PERF-01, ASM-07, ASM-12.
class RegistrationStatusService:
    """Count responses and retain the latest calculated registration status."""

    def __init__(
        self,
        count_service: RegistrationCountService,
        form_settings: GoogleFormSettings | None = None,
    ) -> None:
        self._count_service = count_service
        self._form_settings = form_settings
        self._snapshots: dict[int | str, RegistrationStatusSnapshot] = {}

    def sync(
        self,
        activity_id: int | str,
        capacity: int,
        google_sheet_id: str,
        range_name: str = "Form Responses 1",
        google_form_url: str = "",
    ) -> RegistrationStatusSnapshot:
        # Supports ASM-08: only replace the snapshot after a successful count read.
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        if not google_sheet_id.strip():
            raise ValueError("google_sheet_id is required")

        response_count = self._count_service.count_responses(
            google_sheet_id,
            range_name,
        )
        if response_count >= capacity and self._form_settings is not None:
            self._form_settings.set_accepting_responses(google_form_url, False)
        snapshot = RegistrationStatusSnapshot(
            activity_id=activity_id,
            response_count=response_count,
            capacity=capacity,
            registration_status=(
                RegistrationStatus.FULL
                if response_count >= capacity
                else RegistrationStatus.AVAILABLE
            ),
            last_successful_sync_at=datetime.now(timezone.utc),
        )
        self._snapshots[activity_id] = snapshot
        return snapshot

    def get(self, activity_id: int | str) -> RegistrationStatusSnapshot | None:
        return self._snapshots.get(activity_id)

from __future__ import annotations

from collections.abc import Iterable
from typing import TYPE_CHECKING, NamedTuple

from backend.app.services.activity_status_sync import ActivityStatusSynchronizer

if TYPE_CHECKING:
    from apscheduler.schedulers.background import BackgroundScheduler


DEFAULT_STATUS_POLL_INTERVAL_SECONDS = 60


class ActivityStatusConfig(NamedTuple):
    activity_id: int | str
    capacity: int
    spreadsheet_id: str
    range_name: str


# Supports FR-SRCH-01 and the IF polling interval constraint.
class ActivityStatusPolling:
    """Run activity status synchronization at a one-minute interval."""

    def __init__(
        self,
        synchronizer: ActivityStatusSynchronizer,
        *,
        poll_interval_seconds: int = DEFAULT_STATUS_POLL_INTERVAL_SECONDS,
        scheduler: BackgroundScheduler | None = None,
    ) -> None:
        if not 60 <= poll_interval_seconds <= 120:
            raise ValueError("poll_interval_seconds must be between 60 and 120")
        self._synchronizer = synchronizer
        self._poll_interval_seconds = poll_interval_seconds
        if scheduler is None:
            from apscheduler.schedulers.background import BackgroundScheduler

            scheduler = BackgroundScheduler()
        self._scheduler = scheduler

    def poll(self, config: ActivityStatusConfig) -> None:
        self._synchronizer.sync(*config)

    def start(self, activities: Iterable[ActivityStatusConfig]) -> None:
        for config in activities:
            self._scheduler.add_job(
                self.poll,
                "interval",
                seconds=self._poll_interval_seconds,
                args=[config],
                id=f"activity-status-{config.activity_id}",
                replace_existing=True,
            )
        self._scheduler.start()

    def stop(self) -> None:
        self._scheduler.shutdown(wait=False)

from __future__ import annotations

from collections.abc import Iterable
from datetime import datetime, timezone
from typing import Any

from apscheduler.schedulers.background import BackgroundScheduler
from googleapiclient.errors import HttpError

from backend.app.models.registration_summary import (
    ActivityRegistrationSummary,
    SyncStatus,
)
from backend.app.services.cache_service import RegistrationCache


DEFAULT_POLL_INTERVAL_SECONDS = 120


# Supports IF-VIEW-01, FR-VIEW-03, NFR-PERF-01, ASM-VIEW-02
class RegistrationPollingWorker:
    """Poll registration sources and save successful snapshots to cache."""

    def __init__(
        self,
        sheets_service: Any,
        cache: RegistrationCache,
        *,
        poll_interval_seconds: int = DEFAULT_POLL_INTERVAL_SECONDS,
        scheduler: BackgroundScheduler | None = None,
    ) -> None:
        if not 60 <= poll_interval_seconds <= 120:
            raise ValueError("poll_interval_seconds must be between 60 and 120")
        self._sheets_service = sheets_service
        self._cache = cache
        self._poll_interval_seconds = poll_interval_seconds
        self._scheduler = scheduler or BackgroundScheduler()

    def poll_activity(
        self,
        activity_id: int | str,
        spreadsheet_id: str,
        range_name: str,
    ) -> ActivityRegistrationSummary | None:
        try:
            registrants = self._sheets_service.fetch_registrants(
                spreadsheet_id,
                range_name,
            )
        except (HttpError, OSError, TimeoutError, ValueError):
            return self._cache.get_failed(activity_id)

        summary = ActivityRegistrationSummary(
            activity_id=activity_id,
            total_registered=len(registrants),
            last_synced_at=datetime.now(timezone.utc),
            sync_status=SyncStatus.SUCCESS,
            cached_responses=registrants,
        )
        self._cache.save(summary)
        return summary

    def start(self, activities: Iterable[tuple[int | str, str, str]]) -> None:
        for activity_id, spreadsheet_id, range_name in activities:
            self._scheduler.add_job(
                self.poll_activity,
                "interval",
                seconds=self._poll_interval_seconds,
                args=[activity_id, spreadsheet_id, range_name],
                id=f"registrants-{activity_id}",
                replace_existing=True,
            )
        self._scheduler.start()

    def stop(self) -> None:
        self._scheduler.shutdown(wait=False)

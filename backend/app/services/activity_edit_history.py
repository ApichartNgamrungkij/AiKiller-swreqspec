from __future__ import annotations

from datetime import datetime, timezone
from typing import Iterable

from backend.app.models.activity_edit_log import ActivityEditLog


# Supports FR-ACT-08, ASM-ACT-06
class ActivityEditHistoryService:
    def record_edit(
        self,
        *,
        activity_id: int,
        editor_id: int,
        field_name: str,
        old_value: str | None,
        new_value: str | None,
        changed_at: datetime | None = None,
    ) -> ActivityEditLog:
        normalized_field = (field_name or "").strip()
        if not normalized_field:
            raise ValueError("field_name is required")
        if activity_id <= 0:
            raise ValueError("activity_id is required")
        if editor_id <= 0:
            raise ValueError("editor_id is required")
        if old_value == new_value:
            raise ValueError("No change detected for this field")

        entry = ActivityEditLog(
            activity_id=activity_id,
            editor_id=editor_id,
            field_name=normalized_field,
            old_value=str(old_value) if old_value is not None else None,
            new_value=str(new_value) if new_value is not None else None,
            changed_at=changed_at or datetime.now(timezone.utc),
        )
        return entry

    # Supports FR-ACT-08, ASM-ACT-06
    def list_for_activity(
        self,
        logs: Iterable[ActivityEditLog],
        *,
        activity_id: int,
    ) -> list[ActivityEditLog]:
        return [log for log in logs if log.activity_id == activity_id]

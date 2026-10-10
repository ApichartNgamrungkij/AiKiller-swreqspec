from __future__ import annotations

from datetime import datetime, timezone
from typing import Iterable

from backend.app.models.activity_audit_log import ActivityActionType, ActivityAuditLog


# Supports FR-DEL-06, NFR-DEL-03, ACC-AUDIT-01, ACC-ADMIN-01, IF-ADMIN-01
class ActivityAuditLogService:
    def record_log(
        self,
        *,
        activity_id: int,
        admin_id: int,
        action_type: str,
        reason: str,
        created_at: datetime | None = None,
    ) -> ActivityAuditLog:
        normalized_action = (action_type or "").strip().lower()
        if normalized_action not in {"delete", "suspend"}:
            raise ValueError("Unsupported action type")
        if not reason or not reason.strip():
            raise ValueError("Reason is required for audit log")

        entry = ActivityAuditLog(
            activity_id=activity_id,
            admin_id=admin_id,
            action_type=ActivityActionType.DELETE
            if normalized_action == "delete"
            else ActivityActionType.SUSPEND,
            reason=reason.strip(),
            created_at=created_at or datetime.now(timezone.utc),
        )
        return entry

    def list_for_activity(
        self,
        logs: Iterable[ActivityAuditLog],
        *,
        activity_id: int,
    ) -> list[ActivityAuditLog]:
        return [
            log
            for log in logs
            if log.activity_id == activity_id
        ]

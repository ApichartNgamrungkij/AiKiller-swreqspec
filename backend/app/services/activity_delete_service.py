from __future__ import annotations

from datetime import datetime, timezone

from backend.app.models.activity import Activity, ActivityStatus
from backend.app.models.activity_audit_log import ActivityActionType, ActivityAuditLog


# Supports FR-DEL-05, FR-DEL-06, IF-HIDE-01, IF-ADMIN-01, ACC-AUDIT-01, NFR-DEL-01, ASM-02, ASM-03
class ActivityDeleteService:
    def delete_or_suspend_activity(
        self,
        activity: Activity,
        *,
        admin_id: int,
        action: str,
        reason: str,
        audit_log_store: list[ActivityAuditLog] | None = None,
    ) -> Activity:
        normalized_action = (action or "").strip().lower()

        if activity.status != ActivityStatus.PUBLISHED:
            raise ValueError("Only published activities can be deleted or suspended")
        if not reason or not reason.strip():
            raise ValueError("Reason is required before confirmation")
        if normalized_action not in {"delete", "suspend"}:
            raise ValueError("Unsupported action")

        activity.status = (
            ActivityStatus.SOFT_DELETED if normalized_action == "delete" else ActivityStatus.HIDDEN
        )
        activity.deleted_at = datetime.now(timezone.utc)
        activity.reason = reason.strip()

        if audit_log_store is not None:
            audit_log_store.append(
                ActivityAuditLog(
                    activity_id=activity.id,
                    admin_id=admin_id,
                    action_type=ActivityActionType.DELETE
                    if normalized_action == "delete"
                    else ActivityActionType.SUSPEND,
                    reason=reason.strip(),
                )
            )

        return activity

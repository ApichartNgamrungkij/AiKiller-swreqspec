from __future__ import annotations

from collections.abc import Mapping
from fastapi import APIRouter, Depends, HTTPException, Request, status
from pydantic import BaseModel

from backend.app.models.activity import Activity
from backend.app.models.activity_audit_log import ActivityAuditLog
from backend.app.services.access_control import (
    AdminAccessError,
    require_admin_access,
    require_https,
)
from backend.app.services.activity_delete_service import ActivityDeleteService

router = APIRouter(prefix="/api/v1/admin/activities", tags=["admin-activities"])

_audit_logs: list[ActivityAuditLog] = []


class ActivityActionRequest(BaseModel):
    action: str
    reason: str
    confirmed: bool = False


def get_current_user() -> Mapping[str, object]:
    raise HTTPException(
        status_code=501, detail="Authentication dependency is not configured"
    )


def get_activity(activity_id: int) -> Activity:
    raise HTTPException(
        status_code=501,
        detail=f"Activity lookup is not configured for activity {activity_id}",
    )


def get_audit_log_store() -> list[ActivityAuditLog]:
    return _audit_logs


@router.post("/{activity_id}/action")
def perform_activity_action(
    activity_id: int,
    payload: ActivityActionRequest,
    request: Request,
    user: Mapping[str, object] = Depends(get_current_user),
    activity: Activity = Depends(get_activity),
    audit_logs: list[ActivityAuditLog] = Depends(get_audit_log_store),
) -> dict[str, object]:
    # Authorization must happen before any activity changes.
    try:
        require_admin_access(user)
    except AdminAccessError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc

    try:
        require_https(headers=dict(request.headers), url=str(request.url))
    except PermissionError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    if activity.id != activity_id:
        raise HTTPException(status_code=404, detail="Activity not found")

    if not payload.confirmed:
        raise HTTPException(status_code=400, detail="Confirmation is required")

    reason = payload.reason.strip() if payload.reason else ""
    if not reason:
        raise HTTPException(status_code=422, detail="Reason is required")

    try:
        admin_id = int(user.get("user_id", user.get("id")))
    except (TypeError, ValueError) as exc:
        raise HTTPException(status_code=403, detail="Invalid admin ID") from exc

    try:
        updated = ActivityDeleteService().delete_or_suspend_activity(
            activity,
            admin_id=admin_id,
            action=payload.action,
            reason=reason,
            audit_log_store=audit_logs,
        )
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    return {
        "activityId": updated.id,
        "status": updated.status.value,
        "action": payload.action.strip().lower(),
        "reason": updated.reason,
        "auditLogRecorded": any(
            log.activity_id == updated.id
            and log.admin_id == admin_id
            and log.reason == reason
            for log in audit_logs
        ),
    }

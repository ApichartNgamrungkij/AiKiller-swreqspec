from __future__ import annotations

from typing import Any, Mapping

from fastapi import APIRouter, Depends, HTTPException, status

from backend.app.models.activity import Activity
from backend.app.services.access_control import can_access_activity_sheet


router = APIRouter(prefix="/activities", tags=["registration"])


def get_current_user() -> Mapping[str, object]:
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Authentication dependency is not configured",
    )


def get_activity(activity_id: int) -> Activity:
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail=f"Activity lookup is not configured for activity {activity_id}",
    )


# Supports ACC-GSHEET-01, ACC-GSHEET-02, NFR-SEC-01, NFR-SEC-02.
@router.get("/{activity_id}/google-sheet-access")
def get_google_sheet_access(
    activity_id: int,
    user: Mapping[str, object] = Depends(get_current_user),
    activity: Activity = Depends(get_activity),
) -> dict[str, Any]:
    if activity.id != activity_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Activity {activity_id} was not found",
        )
    if not can_access_activity_sheet(user, activity):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="ไม่มีสิทธิ์เข้าถึง Google Sheets ของกิจกรรมนี้",
        )
    return {
        "activityId": activity_id,
        "canAccess": True,
    }

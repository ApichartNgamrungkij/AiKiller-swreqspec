from __future__ import annotations

from typing import Any, Mapping
from urllib.parse import urlparse

from fastapi import APIRouter, Depends, HTTPException, status

from backend.app.models.activity import Activity
from backend.app.models.activity_export_source import ActivityExportSource
from backend.app.services.access_control import can_access_activity_sheet


router = APIRouter(prefix="/activities", tags=["export"])


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


def get_export_source(activity_id: int) -> ActivityExportSource:
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail=f"Export source lookup is not configured for activity {activity_id}",
    )


# Supports FR-EXP-02, IF-EXPORT-01, IF-GSHEET-01, ACC-GSHEET-01, ACC-GSHEET-02, ASM-05.
@router.get("/{activity_id}/google-sheet")
def get_google_sheet(
    activity_id: int,
    user: Mapping[str, object] = Depends(get_current_user),
    activity: Activity = Depends(get_activity),
    source: ActivityExportSource = Depends(get_export_source),
) -> dict[str, Any]:
    if activity.id != activity_id or source.activity_id != activity_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Activity {activity_id} was not found",
        )
    if not can_access_activity_sheet(user, activity):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="ไม่มีสิทธิ์เข้าถึง Google Sheets ของกิจกรรมนี้",
        )
    parsed_url = urlparse(source.google_sheet_url.strip())
    if parsed_url.scheme not in {"http", "https"} or not parsed_url.netloc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="ไม่สามารถเปิด Google Sheets ได้ เนื่องจากลิงก์ไม่พร้อมใช้งาน",
        )
    return {
        "activityId": activity_id,
        "googleSheetUrl": source.google_sheet_url,
    }

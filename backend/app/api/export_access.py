from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status

from backend.app.integrations.google_sheets import GoogleSheetsClient
from backend.app.models.activity import Activity
from backend.app.models.activity_export_source import ActivityExportSource
from backend.app.services.access_control import can_access_activity_sheet
from backend.app.services.export_source_service import ExportSourceService


router = APIRouter(prefix="/activities", tags=["export"])


def get_current_user() -> dict[str, object]:
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


def get_google_sheets_client() -> GoogleSheetsClient:
    return GoogleSheetsClient()


def get_export_source_service(
    source: ActivityExportSource = Depends(get_export_source),
    google_sheets: GoogleSheetsClient = Depends(get_google_sheets_client),
) -> ExportSourceService:
    return ExportSourceService(google_sheets, {source.activity_id: source})


# Supports FR-EXP-01, IF-GSHEET-01, CON-EXPORT-01, ASM-01, ASM-06.
@router.get("/{activity_id}/export-access")
def get_export_access(
    activity_id: int,
    user: dict[str, object] = Depends(get_current_user),
    activity: Activity = Depends(get_activity),
    source: ActivityExportSource = Depends(get_export_source),
    service: ExportSourceService = Depends(get_export_source_service),
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
    try:
        snapshot = service.read_latest(
            activity_id,
            spreadsheet_id=source.google_sheet_url.rsplit("/", 1)[-1],
        )
    except LookupError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error)) from error
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=str(error)) from error

    response: dict[str, Any] = {
        "activityId": snapshot.activity_id,
        "canExport": snapshot.can_export,
        "responseCount": snapshot.response_count,
        "lastSuccessfulReadAt": snapshot.last_successful_read_at,
    }
    if snapshot.can_export:
        response["googleSheetUrl"] = snapshot.google_sheet_url
    return response

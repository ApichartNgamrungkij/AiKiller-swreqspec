from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status

from backend.app.models.activity import Activity
from backend.app.services.registration_status_service import RegistrationStatusService


router = APIRouter(prefix="/activities", tags=["registration"])


def get_activity(activity_id: int) -> Activity:
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail=f"Activity lookup is not configured for activity {activity_id}",
    )


def get_registration_status_service() -> RegistrationStatusService:
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Registration status service is not configured",
    )


# Supports FR-REG-04, FR-REG-05, FR-REG-06, IF-GFORM-02, NFR-PERF-01, ASM-07, ASM-12.
@router.post("/{activity_id}/registration-sync")
def sync_registration_status(
    activity_id: int,
    activity: Activity = Depends(get_activity),
    service: RegistrationStatusService = Depends(get_registration_status_service),
) -> dict[str, Any]:
    if activity.activity_id not in (None, activity_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Activity {activity_id} was not found",
        )
    snapshot = service.sync(
        activity_id,
        activity.capacity,
        activity.google_sheet_id,
        google_form_url=activity.google_form_url,
    )
    activity.registration_status = snapshot.registration_status
    return {
        "activityId": snapshot.activity_id,
        "responseCount": snapshot.response_count,
        "capacity": snapshot.capacity,
        "registrationStatus": snapshot.registration_status.value,
        "lastSuccessfulSyncAt": snapshot.last_successful_sync_at,
    }

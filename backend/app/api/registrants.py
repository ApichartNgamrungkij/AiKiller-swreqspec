from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status

from backend.app.api.deps import verify_event_owner_or_admin
from backend.app.models.activity import Activity
from backend.app.models.registration_summary import ActivityRegistrationSummary, SyncStatus
from backend.app.schemas.registrant import RegistrantsResponse
from backend.app.services.cache_service import RegistrationCache


router = APIRouter(prefix="/api/v1/activities", tags=["registrants"])
_registration_cache = RegistrationCache()


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


def get_registration_cache() -> RegistrationCache:
    return _registration_cache


def _empty_summary(activity_id: int) -> ActivityRegistrationSummary:
    return ActivityRegistrationSummary(
        activity_id=activity_id,
        total_registered=0,
        last_synced_at=None,
        sync_status=SyncStatus.SUCCESS,
    )


# Supports FR-VIEW-01, FR-VIEW-02, FR-VIEW-03, FR-VIEW-04, FR-VIEW-05, NFR-SEC-02
@router.get("/{activity_id}/registrants", response_model=RegistrantsResponse)
def get_registrants(
    activity_id: int,
    user: Mapping[str, object] = Depends(get_current_user),
    activity: Activity = Depends(get_activity),
    cache: RegistrationCache = Depends(get_registration_cache),
) -> RegistrantsResponse:
    verify_event_owner_or_admin(user, activity)
    summary = cache.get(activity_id) or _empty_summary(activity_id)
    is_cache = summary.sync_status is SyncStatus.FAILED
    return RegistrantsResponse(
        activityId=summary.activity_id,
        totalRegistered=summary.total_registered,
        lastSyncedAt=summary.last_synced_at,
        syncStatus=summary.sync_status.value,
        isCache=is_cache,
        data=[item.to_dict() for item in summary.cached_responses],
    )

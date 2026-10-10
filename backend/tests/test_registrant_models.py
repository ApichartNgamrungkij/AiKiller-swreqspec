from datetime import datetime, timezone

import pytest

from backend.app.models.registrant import RegisteredStudent
from backend.app.models.registration_summary import (
    ActivityRegistrationSummary,
    SyncStatus,
)


# Supports FR-VIEW-02, FR-VIEW-03, FR-VIEW-04, CON-VIEW-01
def test_registration_models_store_required_student_and_summary_fields() -> None:
    student = RegisteredStudent(
        row_id=1,
        timestamp=datetime(2026, 10, 10, 8, 30, tzinfo=timezone.utc),
        student_id="660510001",
        full_name="นายสมชาย ใจดี",
        faculty="วิศวกรรมศาสตร์",
        email="student@example.com",
    )
    summary = ActivityRegistrationSummary(
        activity_id="ACT-001",
        total_registered=1,
        last_synced_at=student.timestamp,
        sync_status=SyncStatus.SUCCESS,
        cached_responses=[student],
    )

    assert student.to_dict()["studentId"] == "660510001"
    assert summary.to_dict() == {
        "activityId": "ACT-001",
        "totalRegistered": 1,
        "lastSyncedAt": student.timestamp,
        "syncStatus": "SUCCESS",
        "cachedResponses": [student.to_dict()],
    }


# Supports CON-VIEW-01
def test_registration_summary_rejects_empty_or_inconsistent_registration_data() -> None:
    with pytest.raises(ValueError, match="total_registered must match"):
        ActivityRegistrationSummary(
            activity_id="ACT-001",
            total_registered=0,
            last_synced_at=None,
            sync_status="FAILED",
            cached_responses=[
                RegisteredStudent(
                    row_id=1,
                    timestamp="2026-10-10T08:30:00Z",
                    student_id="660510001",
                    full_name="นายสมชาย ใจดี",
                )
            ],
        )

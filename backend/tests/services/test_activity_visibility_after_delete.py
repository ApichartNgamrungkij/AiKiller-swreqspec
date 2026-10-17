
import pytest

from backend.app.models.activity import Activity, ActivityStatus
from backend.app.models.activity_audit_log import ActivityAuditLog
from backend.app.services.activity_delete_service import ActivityDeleteService
from backend.app.services.activity_service import student_search_results


@pytest.mark.parametrize(
    ("action", "expected_status"),
    [
        ("delete", ActivityStatus.SOFT_DELETED),
        ("suspend", ActivityStatus.HIDDEN),
    ],
)
def test_action_hides_activity_from_student_results(action, expected_status):
    target = Activity(
        id=7,
        title="Activity to remove",
        status=ActivityStatus.PUBLISHED,
    )
    unrelated = Activity(
        id=8,
        title="Unrelated published activity",
        status=ActivityStatus.PUBLISHED,
    )
    activities = [target, unrelated]
    audit_logs: list[ActivityAuditLog] = []

    ActivityDeleteService().delete_or_suspend_activity(
        target,
        admin_id=10,
        action=action,
        reason="Test reason",
        audit_log_store=audit_logs,
    )

    results = student_search_results(
        activities,
        user={"role": "student"},
    )

    assert target.status == expected_status
    assert all(item["id"] != target.id for item in results)
    assert [item["id"] for item in results] == [unrelated.id]
    assert unrelated.status == ActivityStatus.PUBLISHED

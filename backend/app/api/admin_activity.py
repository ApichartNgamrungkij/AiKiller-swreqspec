from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Iterable, Mapping

from backend.app.models.activity import Activity, ActivityStatus
from backend.app.models.activity_audit_log import ActivityActionType, ActivityAuditLog
from backend.app.services.activity_audit_log_service import ActivityAuditLogService
from backend.app.services.activity_delete_service import ActivityDeleteService
from backend.app.services.activity_visibility_service import student_activity_list


# Supports FR-DEL-01, FR-DEL-02, IF-ADMIN-01, CON-DEL-01
@dataclass(frozen=True)
class ActivityAction:
    label: str
    action: str


# Supports FR-DEL-03, FR-DEL-04, IF-REASON-01, ASM-01
def validate_delete_reason(reason: str | None) -> str | None:
    if reason is None or not reason.strip():
        return "กรุณาระบุเหตุผลก่อนยืนยันการลบ/ระงับกิจกรรม"
    return None


def can_admin_manage_activity(activity: Mapping[str, object]) -> bool:
    return str(activity.get("status", "")).lower() == "published"


def get_available_actions(activity: Mapping[str, object]) -> tuple[ActivityAction, ...]:
    if not can_admin_manage_activity(activity):
        return ()
    return (
        ActivityAction(label="ลบ", action="delete"),
        ActivityAction(label="ระงับ", action="suspend"),
    )


def list_admin_activities(activities: Iterable[Mapping[str, object]]) -> list[dict[str, object]]:
    active_activities: list[dict[str, object]] = []
    for activity in activities:
        if can_admin_manage_activity(activity):
            active_activities.append(
                {
                    "id": activity.get("id"),
                    "title": activity.get("title"),
                    "status": activity.get("status"),
                    "actions": get_available_actions(activity),
                }
            )
    return active_activities


def confirm_activity_action(activity: Mapping[str, object], action: str, reason: str | None) -> tuple[bool, str | None]:
    if not can_admin_manage_activity(activity):
        return False, "กิจกรรมนี้ไม่อยู่ในสถานะที่สามารถลบหรือระงับได้"

    error = validate_delete_reason(reason)
    if error:
        return False, error

    if action not in {"delete", "suspend"}:
        return False, "การดำเนินการไม่ถูกต้อง"

    return True, None


# Supports FR-DEL-06, NFR-DEL-03, ACC-AUDIT-01, ACC-ADMIN-01, IF-ADMIN-01
def record_activity_audit_log(
    *,
    activity_id: int,
    admin_id: int,
    action_type: str,
    reason: str,
    created_at: datetime | None = None,
) -> ActivityAuditLog:
    return ActivityAuditLogService().record_log(
        activity_id=activity_id,
        admin_id=admin_id,
        action_type=action_type,
        reason=reason,
        created_at=created_at,
    )


# Supports FR-DEL-06, NFR-DEL-03, ACC-AUDIT-01, ACC-ADMIN-01, IF-ADMIN-01
def get_activity_audit_logs(logs: list[ActivityAuditLog], *, activity_id: int) -> list[ActivityAuditLog]:
    return ActivityAuditLogService().list_for_activity(logs, activity_id=activity_id)


def handle_activity_action(
    activity: Activity,
    *,
    admin_id: int,
    action: str,
    reason: str,
    audit_log_store: list[ActivityAuditLog] | None = None,
) -> Activity:
    service = ActivityDeleteService()
    return service.delete_or_suspend_activity(
        activity,
        admin_id=admin_id,
        action=action,
        reason=reason,
        audit_log_store=audit_log_store,
    )


def test_AC_DEL_01_admin_can_choose_delete_or_suspend_only_for_published_activities() -> None:
    activities = [
        {"id": 1, "title": "กิจกรรม A", "status": "published"},
        {"id": 2, "title": "กิจกรรม B", "status": "hidden"},
        {"id": 3, "title": "กิจกรรม C", "status": "published"},
    ]

    published = list_admin_activities(activities)

    assert [entry["id"] for entry in published] == [1, 3]
    assert [action.action for action in published[0]["actions"]] == ["delete", "suspend"]
    assert get_available_actions({"status": "hidden"}) == ()
    assert can_admin_manage_activity({"status": "published"}) is True
    assert can_admin_manage_activity({"status": "hidden"}) is False


def test_AC_DEL_02_and_AC_DEL_03_reason_is_required_before_confirmation() -> None:
    activity = {"id": 10, "title": "กิจกรรม A", "status": "published"}

    ok, message = confirm_activity_action(activity, "delete", "เนื้อหาผิดกฎหมาย")
    assert ok is True
    assert message is None

    ok, message = confirm_activity_action(activity, "suspend", " ")
    assert ok is False
    assert message == "กรุณาระบุเหตุผลก่อนยืนยันการลบ/ระงับกิจกรรม"

    ok, message = confirm_activity_action({"status": "hidden"}, "delete", "เหตุผล")
    assert ok is False
    assert message == "กิจกรรมนี้ไม่อยู่ในสถานะที่สามารถลบหรือระงับได้"


def test_AC_DEL_04_student_activity_list_excludes_hidden_or_soft_deleted_activities() -> None:
    visible_items = [
        Activity(id=1, title="Open", status=ActivityStatus.PUBLISHED),
        Activity(id=2, title="Hidden", status=ActivityStatus.HIDDEN),
        Activity(id=3, title="Deleted", status=ActivityStatus.SOFT_DELETED),
    ]

    shown = student_activity_list(visible_items)
    assert [item.id for item in shown] == [1]
    assert shown[0].is_visible_to_students is True


def test_AC_DEL_05_audit_log_is_created_when_activity_is_removed_or_suspended() -> None:
    audit_log_store: list[ActivityAuditLog] = []
    activity = Activity(id=7, title="Need review", status=ActivityStatus.PUBLISHED)

    updated = handle_activity_action(
        activity,
        admin_id=99,
        action="delete",
        reason="เนื้อหาผิดกฎหมาย",
        audit_log_store=audit_log_store,
    )

    assert updated.status == ActivityStatus.SOFT_DELETED
    assert updated.reason == "เนื้อหาผิดกฎหมาย"
    assert len(audit_log_store) == 1
    assert audit_log_store[0].admin_id == 99
    assert audit_log_store[0].action_type == ActivityActionType.DELETE
    assert audit_log_store[0].reason == "เนื้อหาผิดกฎหมาย"

    recorded = record_activity_audit_log(
        activity_id=7,
        admin_id=88,
        action_type="suspend",
        reason="ระงับชั่วคราว",
        created_at=datetime.now(timezone.utc),
    )
    history = get_activity_audit_logs([audit_log_store[0], recorded], activity_id=7)

    assert len(history) == 2
    assert history[0].admin_id == 99
    assert history[1].admin_id == 88
    assert history[1].action_type == ActivityActionType.SUSPEND
    assert history[1].created_at is not None

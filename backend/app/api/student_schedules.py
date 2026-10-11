from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

from backend.app.models.personal_busy_period import PersonalBusyPeriod
from backend.app.routes.me_schedule import get_my_schedule


# Supports FR-SRCH-02, FR-SRCH-03, IF — ตารางส่วนตัวต้องใช้ข้อมูลที่นักศึกษากรอกเองเท่านั้นและต้องมีการตรวจสิทธิ์ก่อนคืนข้อมูล
def get_student_schedule(
    user: Mapping[str, Any] | None,
    *,
    store: Sequence[PersonalBusyPeriod | Mapping[str, Any]] | None = None,
) -> dict[str, Any]:
    return get_my_schedule(user, store=store)


# Supports FR-SRCH-02, FR-SRCH-03
def list_student_schedule(
    user: Mapping[str, Any] | None,
    *,
    store: Sequence[PersonalBusyPeriod | Mapping[str, Any]] | None = None,
) -> list[dict[str, Any]]:
    response = get_student_schedule(user, store=store)
    return list(response.get("schedule", []))


my_schedule = get_student_schedule

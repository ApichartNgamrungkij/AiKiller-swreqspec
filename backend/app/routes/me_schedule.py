from __future__ import annotations

from typing import Any, Mapping


# Supports CON-SCHED-01, FR-SCHED-01
def is_authenticated_student(user: Mapping[str, Any] | None) -> bool:
    if not user:
        return False

    if isinstance(user.get("is_authenticated"), bool):
        return user["is_authenticated"]

    if isinstance(user.get("logged_in"), bool):
        return user["logged_in"]

    role = str(user.get("role", "")).strip().lower()
    if role == "student":
        return True

    return user.get("student_id") is not None or user.get("id") is not None


# Supports CON-SCHED-01, FR-SCHED-01
def require_student_access(user: Mapping[str, Any] | None) -> None:
    if not is_authenticated_student(user):
        raise PermissionError("กรุณาเข้าสู่ระบบก่อนใช้งานตารางของฉัน")


# Supports FR-SCHED-01, CON-SCHED-01
def get_my_schedule(user: Mapping[str, Any] | None) -> dict[str, Any]:
    require_student_access(user)
    student_id = user.get("student_id") if user is not None else None
    return {
        "student_id": student_id,
        "schedule": [],
        "status": "authorized",
    }

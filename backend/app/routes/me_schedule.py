from __future__ import annotations

from typing import Any, Mapping, Sequence

from backend.app.models.personal_busy_period import PersonalBusyPeriod


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


# Supports FR-SCHED-03, IF-SCHED-01
def _current_student_id(user: Mapping[str, Any] | None) -> Any:
    if user is None:
        return None
    return user.get("student_id") if user.get("student_id") is not None else user.get("id")


# Supports FR-SCHED-03, IF-SCHED-01
def _normalize_busy_periods(entries: Sequence[PersonalBusyPeriod | Mapping[str, Any]]) -> list[PersonalBusyPeriod]:
    normalized: list[PersonalBusyPeriod] = []
    for entry in entries:
        if isinstance(entry, PersonalBusyPeriod):
            normalized.append(entry)
        elif isinstance(entry, Mapping):
            normalized.append(PersonalBusyPeriod.from_dict(dict(entry)))
        else:
            raise TypeError(f"Unsupported busy period entry: {entry!r}")
    return normalized


# Supports FR-SCHED-01, FR-SCHED-03, IF-SCHED-01
def get_my_schedule(
    user: Mapping[str, Any] | None,
    *,
    store: Sequence[PersonalBusyPeriod | Mapping[str, Any]] | None = None,
) -> dict[str, Any]:
    require_student_access(user)
    student_id = _current_student_id(user)
    periods = _normalize_busy_periods(store or []) if store is not None else []
    if store is not None:
        periods = [period for period in periods if period.student_id == student_id]
    return {
        "student_id": student_id,
        "schedule": [period.to_dict() for period in periods],
        "status": "authorized",
    }


# Supports FR-SCHED-02, FR-SCHED-03, IF-SCHED-01
def create_busy_period(
    user: Mapping[str, Any] | None,
    payload: Mapping[str, Any],
    *,
    store: list[PersonalBusyPeriod | Mapping[str, Any]] | None = None,
) -> dict[str, Any]:
    require_student_access(user)
    student_id = _current_student_id(user)
    current_store = [] if store is None else list(store)
    period = PersonalBusyPeriod.from_dict(dict(payload)).with_student_id(student_id)
    current_store.append(period)
    return get_my_schedule(user, store=current_store)


# Supports FR-SCHED-02, FR-SCHED-03, IF-SCHED-01
def update_busy_period(
    user: Mapping[str, Any] | None,
    period_id: Any,
    payload: Mapping[str, Any],
    *,
    store: list[PersonalBusyPeriod | Mapping[str, Any]] | None = None,
) -> dict[str, Any]:
    require_student_access(user)
    student_id = _current_student_id(user)
    current_store = [] if store is None else list(store)
    normalized = _normalize_busy_periods(current_store)
    updated = PersonalBusyPeriod.from_dict(dict(payload)).with_student_id(student_id)
    updated.id = period_id

    rebuilt: list[PersonalBusyPeriod] = []
    replaced = False
    for period in normalized:
        if period.id == period_id and period.student_id == student_id:
            rebuilt.append(updated)
            replaced = True
        else:
            rebuilt.append(period)

    if not replaced:
        rebuilt.append(updated)

    return get_my_schedule(user, store=rebuilt)

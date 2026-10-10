from __future__ import annotations

import pytest

from backend.app.routes.me_schedule import get_my_schedule, is_authenticated_student, require_student_access


# Supports AC-SCHED-01, CON-SCHED-01, FR-SCHED-01
def test_AC_SCHED_01_open_schedule_after_login() -> None:
    assert is_authenticated_student({"is_authenticated": True}) is True
    assert is_authenticated_student({"role": "student"}) is True
    assert is_authenticated_student({"role": "guest"}) is False
    assert is_authenticated_student({}) is False

    allowed = get_my_schedule({"student_id": "S-001", "is_authenticated": True})
    assert allowed["status"] == "authorized"
    assert allowed["student_id"] == "S-001"
    assert allowed["schedule"] == []

    with pytest.raises(PermissionError, match="เข้าสู่ระบบ"):
        require_student_access({})

    with pytest.raises(PermissionError, match="เข้าสู่ระบบ"):
        get_my_schedule({})

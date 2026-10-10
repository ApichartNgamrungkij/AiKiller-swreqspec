from __future__ import annotations

import pytest

from backend.app.services.access_control import (
    AdminAccessError,
    is_admin_user,
    is_https_request,
    require_admin_access,
    require_https,
)


# Supports AC-DEL-06, FR-DEL-07, IF-ADMIN-01, ACC-ADMIN-01
def test_AC_DEL_06_non_admin_users_cannot_open_or_confirm_delete_actions() -> None:
    assert is_admin_user({"role": "admin"}) is True
    assert is_admin_user({"is_admin": True}) is True
    assert is_admin_user({"role": "student"}) is False
    assert is_admin_user({}) is False

    with pytest.raises(AdminAccessError, match="Only admins can"):
        require_admin_access({"role": "student"}, action="open the delete form")

    with pytest.raises(AdminAccessError, match="Only admins can"):
        require_admin_access({"is_admin": False}, action="confirm delete or suspend")


# Supports NFR-DEL-02
def test_AC_DEL_06_https_is_required_for_delete_or_suspend_requests() -> None:
    assert is_https_request(headers={"x-forwarded-proto": "https"}) is True
    assert is_https_request(url="https://example.com/admin/activities/1/delete") is True
    assert is_https_request(headers={"x-forwarded-proto": "http"}) is False
    assert is_https_request(url="http://example.com/admin/activities/1/delete") is False

    require_https(headers={"x-forwarded-proto": "https"})
    require_https(url="https://example.com/admin/activities/1/delete")

    with pytest.raises(PermissionError, match="HTTPS is required"):
        require_https(headers={"x-forwarded-proto": "http"})

    with pytest.raises(PermissionError, match="HTTPS is required"):
        require_https(url="http://example.com/admin/activities/1/delete")

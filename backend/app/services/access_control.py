from __future__ import annotations

from typing import Any, Mapping
from urllib.parse import urlparse


class AdminAccessError(PermissionError):
    """Raised when a non-admin user attempts to manage activity deletion."""


# Supports ACC-VIEW-01, ACC-VIEW-02, FR-VIEW-05, NFR-SEC-02
def is_activity_owner(
    user: Mapping[str, object] | None,
    activity: Mapping[str, object] | Any,
) -> bool:
    if user is None:
        return False
    user_id = user.get("user_id")
    owner_id = (
        activity.get("owner_id")
        if isinstance(activity, Mapping)
        else getattr(activity, "owner_id", None)
    )
    if user_id is None or owner_id is None:
        return False
    return str(user_id) == str(owner_id)


# Supports FR-DEL-07, NFR-DEL-01, NFR-DEL-02, ACC-ADMIN-01, IF-ADMIN-01
def is_admin_user(user: Mapping[str, object] | None) -> bool:
    if not user:
        return False

    role_value = user.get("role")
    if isinstance(role_value, str):
        normalized = role_value.strip().lower()
        if normalized in {"admin", "administrator", "system_admin"}:
            return True
        if normalized in {"student", "user", "guest"}:
            return False

    is_admin_value = user.get("is_admin")
    if isinstance(is_admin_value, bool):
        return is_admin_value

    access_value = user.get("access")
    if isinstance(access_value, str):
        normalized_access = access_value.strip().lower()
        return normalized_access in {"admin", "administrator", "system_admin"}

    return False


# Supports FR-DEL-07, NFR-DEL-01, ACC-ADMIN-01, IF-ADMIN-01
def require_admin_access(user: Mapping[str, object] | None, *, action: str = "delete or suspend activities") -> None:
    if not is_admin_user(user):
        raise AdminAccessError(f"Only admins can {action}")


# Supports NFR-DEL-02
def is_https_request(
    *,
    headers: Mapping[str, str] | None = None,
    url: str | None = None,
) -> bool:
    if url:
        scheme = urlparse(url).scheme.lower()
        if scheme == "https":
            return True
        if scheme == "http":
            return False

    if not headers:
        return False

    forwarded_proto = headers.get("x-forwarded-proto") or headers.get("X-Forwarded-Proto") or ""
    if forwarded_proto:
        return any(part.strip().lower() == "https" for part in forwarded_proto.split(","))

    forwarded_scheme = headers.get("x-forwarded-scheme") or headers.get("X-Forwarded-Scheme") or ""
    if forwarded_scheme:
        return forwarded_scheme.strip().lower() == "https"

    scheme = headers.get("scheme") or headers.get("Scheme") or ""
    if scheme:
        return scheme.strip().lower() == "https"

    origin = headers.get("origin") or headers.get("Origin") or ""
    if origin:
        return urlparse(origin).scheme.lower() == "https"

    return False


# Supports NFR-DEL-02
def require_https(
    *,
    headers: Mapping[str, str] | None = None,
    url: str | None = None,
) -> None:
    if not is_https_request(headers=headers, url=url):
        raise PermissionError("HTTPS is required for delete or suspend requests")

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class AccessRole(StrEnum):
    ADMIN = "admin"
    ORGANIZER = "organizer"
    STUDENT = "student"


# Supports ACC-GSHEET-01, ACC-GSHEET-02, NFR-SEC-01, NFR-SEC-02.
@dataclass(frozen=True, slots=True)
class AccessRoleAssignment:
    """Associate a user's role with an activity for access checks."""

    user_id: str
    role: AccessRole
    activity_id: int


# Supports ACC-GSHEET-01, ACC-GSHEET-02, NFR-SEC-01, NFR-SEC-02.
@dataclass(frozen=True, slots=True)
class ActivitySheetAccess:
    """The minimum access decision needed before exposing a sheet reference."""

    user_id: str
    activity_id: int
    role: AccessRole

    @property
    def allowed(self) -> bool:
        return self.role in {AccessRole.ADMIN, AccessRole.ORGANIZER}

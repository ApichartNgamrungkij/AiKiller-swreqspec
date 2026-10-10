from __future__ import annotations

import pytest

from backend.app.routes.activity import (  # noqa: F401
    ActivityCreatorAccessError,
    is_authorized_activity_creator,
    require_activity_creator_access,
)


# Supports AC-ACT-01
def test_AC_ACT_01_only_approved_organizers_can_open_create_activity_page() -> None:
    assert is_authorized_activity_creator({"role": "organizer"}) is True
    assert is_authorized_activity_creator({"can_create_activity": True}) is True
    assert is_authorized_activity_creator({"approved_by_admin": True}) is True
    assert is_authorized_activity_creator({"role": "student"}) is False
    assert is_authorized_activity_creator({}) is False

    with pytest.raises(ActivityCreatorAccessError, match="ได้รับสิทธิ์จาก Admin"):
        require_activity_creator_access({})

    require_activity_creator_access({"role": "organizer"})
    require_activity_creator_access({"approved_by_admin": True})

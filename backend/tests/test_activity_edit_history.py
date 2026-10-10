from __future__ import annotations

import pytest

from backend.app.services.activity_edit_history import ActivityEditHistoryService


# Supports AC-ACT-08
def test_AC_ACT_08_activity_edit_history_records_each_change() -> None:
    service = ActivityEditHistoryService()

    entry = service.record_edit(
        activity_id=7,
        editor_id=42,
        field_name="venue",
        old_value="หอประชุมเล็ก",
        new_value="หอประชุมใหญ่",
    )

    assert entry.activity_id == 7
    assert entry.editor_id == 42
    assert entry.field_name == "venue"
    assert entry.old_value == "หอประชุมเล็ก"
    assert entry.new_value == "หอประชุมใหญ่"
    assert service.list_for_activity([entry], activity_id=7) == [entry]

    with pytest.raises(ValueError, match="No change detected"):
        service.record_edit(
            activity_id=7,
            editor_id=42,
            field_name="venue",
            old_value="same",
            new_value="same",
        )

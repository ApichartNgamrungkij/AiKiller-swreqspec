from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class RegisteredStudentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    row_id: int | str = Field(alias="rowId")
    timestamp: datetime | str
    student_id: str = Field(alias="studentId")
    full_name: str = Field(alias="fullName")
    faculty: str | None = None
    email: str | None = None


class RegistrantsResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    activity_id: int | str = Field(alias="activityId")
    total_registered: int = Field(alias="totalRegistered")
    last_synced_at: datetime | str | None = Field(alias="lastSyncedAt")
    sync_status: str = Field(alias="syncStatus")
    is_cache: bool = Field(alias="isCache")
    data: list[RegisteredStudentResponse]

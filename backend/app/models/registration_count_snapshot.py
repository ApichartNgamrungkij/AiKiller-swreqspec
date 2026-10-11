from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.models.activity import Base


# Supports FR-REG-04, FR-REG-05, FR-REG-06, NFR-PERF-01.
class RegistrationCountSnapshot(Base):
    """Store the last successful registration count for an activity."""

    __tablename__ = "registration_count_snapshots"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    activity_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    response_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    last_successful_sync_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Optional

from sqlalchemy import DateTime, String, Text, Enum as SQLEnum
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


# Supports FR-DEL-01, FR-DEL-05, IF-HIDE-01, CON-DEL-01, ASM-02, ASM-03
class ActivityStatus(str, Enum):
    PUBLISHED = "published"
    HIDDEN = "hidden"
    SOFT_DELETED = "soft_deleted"


class Base(DeclarativeBase):
    pass


# Supports FR-DEL-01, FR-DEL-05, IF-HIDE-01, CON-DEL-01, ASM-02, ASM-03
class Activity(Base):
    __tablename__ = "activities"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[ActivityStatus] = mapped_column(
        SQLEnum(ActivityStatus, native_enum=False, name="activity_status"),
        nullable=False,
        default=ActivityStatus.PUBLISHED,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    @property
    def is_visible_to_students(self) -> bool:
        return self.status == ActivityStatus.PUBLISHED

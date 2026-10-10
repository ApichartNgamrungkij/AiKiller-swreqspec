from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum

from sqlalchemy import DateTime, Enum as SQLEnum, Text
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.models.activity import Base


# Supports FR-DEL-06, ACC-AUDIT-01, NFR-DEL-03
class ActivityActionType(str, Enum):
    DELETE = "delete"
    SUSPEND = "suspend"


# Supports FR-DEL-06, ACC-AUDIT-01, NFR-DEL-03
class ActivityAuditLog(Base):
    __tablename__ = "activity_audit_logs"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    activity_id: Mapped[int] = mapped_column(nullable=False, index=True)
    admin_id: Mapped[int] = mapped_column(nullable=False, index=True)
    action_type: Mapped[ActivityActionType] = mapped_column(
        SQLEnum(ActivityActionType, native_enum=False, name="activity_action_type"),
        nullable=False,
    )
    reason: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

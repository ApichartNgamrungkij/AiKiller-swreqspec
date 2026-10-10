from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime, time, timezone
from enum import Enum
from typing import Any, Optional
from urllib.parse import urlparse

from sqlalchemy import DateTime, Integer, String, Text, Enum as SQLEnum
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from backend.app.models.activity_slot import ActivitySlot


# Supports FR-DEL-01, FR-DEL-05, IF-HIDE-01, CON-DEL-01, ASM-02, ASM-03
class ActivityStatus(str, Enum):
    PUBLISHED = "published"
    HIDDEN = "hidden"
    SOFT_DELETED = "soft_deleted"


# Supports FR-ACT-02, DOM-ACT-01, IF-ACT-01, IF-ACT-02, ASM-ACT-03, ASM-ACT-05
class ActivityCategory(str, Enum):
    ACADEMIC = "วิชาการ"
    SPORTS = "กีฬา"
    ARTS = "ศิลปวัฒนธรรม"
    ETHICS = "คุณธรรมจริยธรรม"
    COMMUNITY_SERVICE = "บำเพ็ญประโยชน์"

    @classmethod
    def normalize(cls, value: str | "ActivityCategory") -> "ActivityCategory":
        if isinstance(value, cls):
            return value
        if value is None:
            raise ValueError("category is required")

        normalized = str(value).strip()
        for item in cls:
            if normalized == item.value or normalized.lower() == item.value.lower():
                return item
        raise ValueError(f"Unsupported activity category: {value}")


class Base(DeclarativeBase):
    pass


# Supports FR-DEL-01, FR-DEL-05, IF-HIDE-01, CON-DEL-01, ASM-02, ASM-03
class Activity(Base):
    __tablename__ = "activities"

    slots: list[Any] = []

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
    category: Mapped[Optional[str]] = mapped_column(String(80), nullable=True, default=ActivityCategory.ACADEMIC.value)
    venue: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, default="")
    max_participants: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, default=0)
    volunteer_hours: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, default=0)
    registration_url: Mapped[Optional[str]] = mapped_column(String(512), nullable=True, default="")

    @property
    def is_visible_to_students(self) -> bool:
        return self.status == ActivityStatus.PUBLISHED


# Supports FR-ACT-02, FR-ACT-03, DOM-ACT-01, IF-ACT-01, IF-ACT-02, ASM-ACT-03, ASM-ACT-05
@dataclass(slots=True)
class ActivityDraft:
    """Create-activity payload used before save: one activity can contain multiple time slots on the same day."""

    title: str
    category: str | ActivityCategory
    venue: str
    max_participants: int
    volunteer_hours: int
    registration_url: str = ""
    slots: list[ActivitySlot] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.title = (self.title or "").strip()
        self.venue = (self.venue or "").strip()
        self.category = ActivityCategory.normalize(self.category)

        if not self.title:
            raise ValueError("title is required")
        if not self.venue:
            raise ValueError("venue is required")
        if self.max_participants <= 0:
            raise ValueError("max_participants must be greater than zero")
        if self.volunteer_hours < 0:
            raise ValueError("volunteer_hours cannot be negative")
        if self.registration_url and not self._is_valid_url(self.registration_url):
            raise ValueError("registration_url must be a valid URL")
        if not self.slots:
            raise ValueError("at least one activity slot is required")

        normalized_slots: list[ActivitySlot] = []
        for slot in self.slots:
            if isinstance(slot, dict):
                normalized_slots.append(ActivitySlot.from_dict(slot))
            else:
                normalized_slots.append(slot)
        self.slots = normalized_slots

    @staticmethod
    def _is_valid_url(value: str) -> bool:
        parsed = urlparse(value)
        return bool(parsed.scheme and parsed.netloc)

    def to_dict(self) -> dict[str, Any]:
        return {
            "title": self.title,
            "category": self.category.value,
            "venue": self.venue,
            "max_participants": self.max_participants,
            "volunteer_hours": self.volunteer_hours,
            "registration_url": self.registration_url,
            "slots": [slot.to_dict() for slot in self.slots],
        }

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "ActivityDraft":
        return cls(
            title=str(payload.get("title") or ""),
            category=payload.get("category") or ActivityCategory.ACADEMIC,
            venue=str(payload.get("venue") or ""),
            max_participants=int(payload.get("max_participants") or 0),
            volunteer_hours=int(payload.get("volunteer_hours") or 0),
            registration_url=str(payload.get("registration_url") or ""),
            slots=[
                ActivitySlot.from_dict(slot) if isinstance(slot, dict) else slot
                for slot in payload.get("slots") or []
            ],
        )

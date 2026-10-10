from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime, time


# Supports FR-ACT-02, IF-ACT-02, ASM-ACT-03, ASM-ACT-05
@dataclass(slots=True)
class ActivitySlot:
    """One time slot for a single activity session, supporting morning/afternoon runs on the same day."""

    id: int | None = None
    activity_id: int | None = None
    slot_date: date | str = field(default_factory=lambda: date.today())
    start_time: time | str = field(default_factory=lambda: time(9, 0))
    end_time: time | str = field(default_factory=lambda: time(10, 0))
    label: str = ""

    def __post_init__(self) -> None:
        self.slot_date = self._coerce_date(self.slot_date)
        self.start_time = self._coerce_time(self.start_time)
        self.end_time = self._coerce_time(self.end_time)

        if self.end_time <= self.start_time:
            raise ValueError("end_time must be later than start_time")

    @staticmethod
    def _coerce_date(value: date | str) -> date:
        if isinstance(value, date):
            return value
        if isinstance(value, str):
            return date.fromisoformat(value)
        raise TypeError(f"Unsupported date value: {value!r}")

    @staticmethod
    def _coerce_time(value: time | str) -> time:
        if isinstance(value, time):
            return value
        if isinstance(value, str):
            try:
                return time.fromisoformat(value)
            except ValueError:
                normalized = value.strip()
                if normalized:
                    parsed = datetime.strptime(normalized, "%H:%M")
                    return parsed.time()
                raise ValueError(f"Unsupported time value: {value!r}")
        raise TypeError(f"Unsupported time value: {value!r}")

    @classmethod
    def from_dict(cls, payload: dict[str, object]) -> "ActivitySlot":
        return cls(
            id=payload.get("id"),
            activity_id=payload.get("activity_id"),
            slot_date=payload.get("slot_date"),
            start_time=payload.get("start_time"),
            end_time=payload.get("end_time"),
            label=str(payload.get("label") or ""),
        )

    def to_dict(self) -> dict[str, object]:
        return {
            "id": self.id,
            "activity_id": self.activity_id,
            "slot_date": self.slot_date.isoformat(),
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat(),
            "label": self.label,
        }

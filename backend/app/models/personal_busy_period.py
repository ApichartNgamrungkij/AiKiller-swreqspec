from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime, time
from typing import Iterable


# Supports FR-SCHED-02, FR-SCHED-03, IF-SCHED-01, ASM-SCHED-02, ASM-SCHED-06
@dataclass(slots=True)
class PersonalBusyPeriod:
    """A recurring personal busy period, repeating daily within the selected date range."""

    id: int | None = None
    student_id: int | str | None = None
    start_date: date | str = field(default_factory=lambda: date.today())
    end_date: date | str = field(default_factory=lambda: date.today())
    start_time: time | str = field(default_factory=lambda: time(9, 0))
    end_time: time | str = field(default_factory=lambda: time(10, 0))

    def __post_init__(self) -> None:
        self.start_date = self._coerce_date(self.start_date)
        self.end_date = self._coerce_date(self.end_date)
        self.start_time = self._coerce_time(self.start_time)
        self.end_time = self._coerce_time(self.end_time)

        if self.end_date < self.start_date:
            raise ValueError("end_date must be on or after start_date")
        if self.end_time <= self.start_time:
            raise ValueError("end_time must be later than start_time")

    @staticmethod
    def _coerce_date(value: date | str) -> date:
        if isinstance(value, date) and not isinstance(value, datetime):
            return value
        if isinstance(value, str):
            return date.fromisoformat(value)
        raise TypeError(f"Unsupported date value: {value!r}")

    @staticmethod
    def _coerce_time(value: time | str) -> time:
        if isinstance(value, time):
            return value
        if isinstance(value, str):
            return time.fromisoformat(value)
        raise TypeError(f"Unsupported time value: {value!r}")

    @classmethod
    def from_dict(cls, payload: dict[str, object]) -> "PersonalBusyPeriod":
        return cls(
            id=payload.get("id"),
            student_id=payload.get("student_id"),
            start_date=payload.get("start_date"),
            end_date=payload.get("end_date"),
            start_time=payload.get("start_time"),
            end_time=payload.get("end_time"),
        )

    def to_dict(self) -> dict[str, object]:
        return {
            "id": self.id,
            "student_id": self.student_id,
            "start_date": self.start_date.isoformat(),
            "end_date": self.end_date.isoformat(),
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat(),
        }

    def dates_in_effect(self) -> list[date]:
        current = self.start_date
        dates: list[date] = []
        while current <= self.end_date:
            dates.append(current)
            current = current.fromordinal(current.toordinal() + 1)
        return dates

    def overlaps_with_activity(self, activity_start: datetime, activity_end: datetime) -> bool:
        if activity_end <= activity_start:
            return False

        activity_day = activity_start.date()
        if activity_day < self.start_date or activity_day > self.end_date:
            return False

        busy_start = datetime.combine(activity_day, self.start_time)
        busy_end = datetime.combine(activity_day, self.end_time)

        return busy_start < activity_end and activity_start < busy_end

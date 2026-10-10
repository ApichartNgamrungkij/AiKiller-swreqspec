from __future__ import annotations

import re
from collections.abc import Sequence
from typing import Any

from backend.app.models.registrant import RegisteredStudent


_HEADER_ALIASES = {
    "row_id": {"rowid", "row", "ลำดับ"},
    "timestamp": {"timestamp", "เวลาประทับ", "ประทับเวลา"},
    "student_id": {"studentid", "รหัสนักศึกษา"},
    "full_name": {"fullname", "ชื่อเต็ม", "ชื่อ-นามสกุล", "ชื่อนามสกุล"},
    "faculty": {"faculty", "คณะ", "คณะ/ภาควิชา"},
    "email": {"email", "อีเมล", "อีเมลนักศึกษา"},
}


def _normalize_header(value: object) -> str:
    return re.sub(r"[\s_\-/]+", "", str(value).strip().lower())


def _header_indexes(headers: Sequence[object]) -> dict[str, int]:
    indexes: dict[str, int] = {}
    normalized_aliases = {
        field: {_normalize_header(alias) for alias in aliases}
        for field, aliases in _HEADER_ALIASES.items()
    }
    for index, header in enumerate(headers):
        normalized_header = _normalize_header(header)
        for field, aliases in normalized_aliases.items():
            if normalized_header in aliases:
                indexes[field] = index
                break

    missing = {"timestamp", "student_id", "full_name"} - indexes.keys()
    if missing:
        raise ValueError(f"Google Sheets response is missing headers: {sorted(missing)}")
    return indexes


def _cell(row: Sequence[object], index: int | None, default: str = "") -> str:
    if index is None or index >= len(row):
        return default
    return str(row[index]).strip()


# Supports IF-VIEW-01, FR-VIEW-02, ASM-VIEW-01
class SheetsService:
    """Fetch and map Google Sheets rows to RegisteredStudent models."""

    def __init__(self, client: Any) -> None:
        self._client = client

    def fetch_registrants(
        self,
        spreadsheet_id: str,
        range_name: str,
    ) -> list[RegisteredStudent]:
        values = self._client.read_values(spreadsheet_id, range_name)
        if not values:
            return []

        indexes = _header_indexes(values[0])
        registrants: list[RegisteredStudent] = []
        for row_number, row in enumerate(values[1:], start=2):
            if not isinstance(row, Sequence) or isinstance(row, (str, bytes)):
                raise ValueError("Google Sheets data rows must be sequences")
            registrants.append(
                RegisteredStudent(
                    row_id=_cell(row, indexes.get("row_id"), str(row_number)),
                    timestamp=_cell(row, indexes["timestamp"]),
                    student_id=_cell(row, indexes["student_id"]),
                    full_name=_cell(row, indexes["full_name"]),
                    faculty=_cell(row, indexes.get("faculty")) or None,
                    email=_cell(row, indexes.get("email")) or None,
                )
            )
        return registrants

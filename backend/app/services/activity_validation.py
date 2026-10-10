from __future__ import annotations

from typing import Any, Mapping
from urllib.parse import urlparse


# Supports DOM-ACT-01, FR-ACT-04, FR-ACT-07, DOM-ACT-02, DOM-ACT-03
APPROVED_ACTIVITY_CATEGORIES = (
    "วิชาการ",
    "กีฬา",
    "ศิลปวัฒนธรรม",
    "คุณธรรมจริยธรรม",
    "บำเพ็ญประโยชน์",
)

_NEW_APPROVAL_KEYS = (
    "approval_required",
    "approval_status",
    "approval_step",
    "new_approval_step",
    "needs_approval",
)


# Supports DOM-ACT-01, FR-ACT-04, FR-ACT-07, DOM-ACT-02, DOM-ACT-03
def normalize_activity_category(value: Any) -> str:
    category = str(value or "").strip()
    if not category:
        raise ValueError("category is required")
    if category not in APPROVED_ACTIVITY_CATEGORIES:
        raise ValueError(f"Unsupported activity category: {value!r}")
    return category


# Supports FR-ACT-04, FR-ACT-07, DOM-ACT-02, DOM-ACT-03
def _has_new_approval_step(payload: Mapping[str, Any]) -> bool:
    if not payload:
        return False
    for key in payload:
        normalized = str(key).strip().lower()
        if normalized in _NEW_APPROVAL_KEYS or normalized.startswith("approval"):
            return True
    return False


# Supports FR-ACT-04, IF-ACT-01, DOM-ACT-01
def validate_activity_submission(payload: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []

    if not payload:
        return ["กรุณากรอกข้อมูลที่จำเป็น"]

    if _has_new_approval_step(payload):
        errors.append("ระบบไม่เพิ่มขั้นตอนอนุมัติใหม่เข้ามาใน workflow")

    required_fields = ["title", "category", "venue", "max_participants", "volunteer_hours"]
    for field_name in required_fields:
        raw_value = payload.get(field_name)
        if raw_value is None or str(raw_value).strip() == "":
            errors.append(f"กรุณากรอกข้อมูล {field_name}")

    if "category" in payload:
        try:
            normalize_activity_category(payload.get("category"))
        except ValueError as exc:
            errors.append(str(exc))

    if "registration_url" in payload and payload.get("registration_url") not in (None, ""):
        parsed = urlparse(str(payload["registration_url"]))
        if not parsed.scheme or not parsed.netloc:
            errors.append("registration_url must be a valid URL")

    slots = payload.get("slots")
    if slots is not None:
        if not isinstance(slots, list) or len(slots) == 0:
            errors.append("กรุณาเพิ่มรอบเวลาอย่างน้อย 1 รอบ")
        else:
            for index, slot in enumerate(slots, start=1):
                if not isinstance(slot, Mapping):
                    errors.append(f"slot_{index} must be an object")
                    continue
                for slot_field in ("slot_date", "start_time", "end_time"):
                    if slot.get(slot_field) in (None, ""):
                        errors.append(f"slot_{index} ต้องมีข้อมูล {slot_field}")

    return errors


# Supports FR-ACT-04, FR-ACT-07, DOM-ACT-02, DOM-ACT-03
def is_valid_activity_submission(payload: Mapping[str, Any]) -> bool:
    return len(validate_activity_submission(payload)) == 0

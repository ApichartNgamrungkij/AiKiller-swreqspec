from __future__ import annotations

from typing import Protocol


class GoogleFormSettings(Protocol):
    """Change whether an activity's Google Form accepts responses."""

    def set_accepting_responses(self, google_form_url: str, accepting: bool) -> None: ...


# Supports IF-GFORM-02, FR-REG-06, ASM-03.
class GoogleFormSettingsClient:
    """Store the response setting for the simulated Google Form."""

    def __init__(self) -> None:
        self._accepting_responses: dict[str, bool] = {}

    def set_accepting_responses(self, google_form_url: str, accepting: bool) -> None:
        if not google_form_url.strip():
            raise ValueError("google_form_url is required")
        self._accepting_responses[google_form_url] = accepting

    def is_accepting_responses(self, google_form_url: str) -> bool:
        if not google_form_url.strip():
            raise ValueError("google_form_url is required")
        return self._accepting_responses.get(google_form_url, True)

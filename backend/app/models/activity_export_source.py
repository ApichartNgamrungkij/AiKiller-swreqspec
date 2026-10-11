from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.models.activity import Base


# Supports FR-EXP-01, FR-EXP-02, IF-GSHEET-01, CON-EXPORT-01.
class ActivityExportSource(Base):
    """Store the Google Sheets source and its last successful read."""

    __tablename__ = "activity_export_sources"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    activity_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    google_sheet_url: Mapped[str] = mapped_column(String(2048), nullable=False)
    last_successful_response_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )
    last_successful_read_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

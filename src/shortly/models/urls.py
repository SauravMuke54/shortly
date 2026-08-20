from datetime import datetime

from sqlalchemy import DateTime, Integer, Sequence, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from shortly.core.database import Base

# Explicit, named sequence so we can pull the next id *before* insert
# and encode it into short_code in the same row — no placeholder, no
# second UPDATE, no race window.
url_id_seq = Sequence("url_id_seq")


class URL(Base):
    __tablename__ = "urls"

    id: Mapped[int] = mapped_column(
        Integer,
        url_id_seq,
        primary_key=True,
        server_default=url_id_seq.next_value(),
    )

    short_code: Mapped[str] = mapped_column(
        String(10),
        unique=True,
        nullable=False,
        index=True,
    )

    original_url: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    expires_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    click_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )
from uuid import uuid4
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import TIMESTAMP, TEXT, BIGINT, UUID
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import expression
from sqlalchemy.types import DateTime
from bot.db.models.base import Base


class utcnow(expression.FunctionElement):
    type = DateTime()
    inherit_cache = True


@compiles(utcnow, 'postgresql')
def pg_utcnow(element, compiler, **kw):
    return "TIMEZONE('utc', CURRENT_TIMESTAMP)"


class User(Base):
    __tablename__ = "users"

    telegram_id: Mapped[int] = mapped_column(
        BIGINT,
        primary_key=True
    )
    fullname: Mapped[str] = mapped_column(
        TEXT,
        nullable=False
    )
    registered_at: Mapped[int] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=utcnow()
    )


class Note(Base):
    __tablename__ = "notes"

    note_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4
    )
    note: Mapped[str] = mapped_column(
        TEXT,
        nullable=False,
    )
    date: Mapped[str] = mapped_column(
        TEXT,
        nullable=False,
    )
    telegram_id: Mapped[int] = mapped_column(
        ForeignKey(
            "users.telegram_id",
            ondelete="CASCADE")
    )
    created_at: Mapped[int] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=utcnow()
    )



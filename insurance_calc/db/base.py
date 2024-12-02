from datetime import datetime

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from insurance_calc.db.meta import meta


class Base(DeclarativeBase):
    """Base for all models."""

    metadata = meta
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    created_date: Mapped[datetime] = mapped_column(default=datetime.now)
    modified_date: Mapped[datetime] = mapped_column(
        default=datetime.now, onupdate=datetime.now
    )

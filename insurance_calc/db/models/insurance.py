from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import Float, String

from insurance_calc.db.base import Base


class Insurance(Base):
    """Main model for calculating insurance rates."""

    __tablename__ = "insurance"

    cargo_type: Mapped[str] = mapped_column(String(64), nullable=False)
    rate: Mapped[float] = mapped_column(Float(), nullable=False)
    date: Mapped[datetime] = mapped_column(String(64), nullable=False)

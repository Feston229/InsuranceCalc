from sqlalchemy.orm import DeclarativeBase
from insurance_calc.db.meta import meta


class Base(DeclarativeBase):
    """Base for all models."""

    metadata = meta


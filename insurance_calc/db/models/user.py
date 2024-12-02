from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import Boolean, String

from insurance_calc.db.base import Base


class Role(Base):
    __tablename__ = "role"

    name: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    users: Mapped[list["User"]] = relationship(
        "User", back_populates="role", cascade="all, delete-orphan"
    )


class User(Base):
    __tablename__ = "user"

    username: Mapped[str] = mapped_column(String(64), unique=True)
    password_hash: Mapped[str] = mapped_column(String(128), nullable=False)
    role_id: Mapped[int] = mapped_column(ForeignKey("role.id"), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), default=False, nullable=False)
    role: Mapped["Role"] = relationship("Role", back_populates="users", lazy="selectin")

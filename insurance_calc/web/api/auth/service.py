import asyncio

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from insurance_calc.db.dependencies import get_db_session
from insurance_calc.db.models.user import Role, User
from insurance_calc.settings import settings
from insurance_calc.web.api.base import BaseService

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="/api/login/access-token")


class UserService(BaseService):
    """Service class for managing users and roles."""

    async def get_role_by_name(self, name: str) -> Role:
        """Retrieve a role by role name."""

        query = select(Role).where(Role.name == name)
        role = await self.session.execute(query)

        return role.scalar_one()

    async def upsert_role(self, id: int, name: str) -> Role:
        """Create a new role."""
        role = Role(id=id, name=name)

        await self.session.merge(role)
        await self.session.commit()

        return role

    async def get_user(self, user_id: int) -> User | None:
        """Retrieve a user by ID."""

        query = select(User).where(User.id == user_id)
        user = await self.session.execute(query)

        return user.scalar_one_or_none()

    async def get_user_by_username(self, username: str) -> User | None:
        """Retrieve a user by username."""

        query = select(User).where(User.username == username)
        user = await self.session.execute(query)

        return user.scalar_one_or_none()

    async def create_user(
        self, username: str, password: str, role: str = "User", is_active: bool = False
    ) -> User:
        """Create a new user."""

        role: Role = await self.get_role_by_name(role)
        password_hash = await asyncio.to_thread(
            CryptContext(schemes=["bcrypt"], deprecated="auto").hash, password
        )
        user: User = User(
            username=username,
            password_hash=password_hash,
            role=role,
            is_active=is_active,
        )

        self.session.add(user)

        await self.session.commit()

        return user

    async def authenticate(self, username: str, password: str) -> User | None:
        user: User | None = await self.get_user_by_username(username)
        if not user:
            return
        password_verified = await asyncio.to_thread(
            CryptContext(schemes=["bcrypt"], deprecated="auto").verify,
            password,
            user.password_hash,
        )
        if not password_verified:
            return
        return user


async def get_user_service(
    session: AsyncSession = Depends(get_db_session),
) -> UserService:
    """Get the user service."""

    return UserService(session)


async def get_current_user(
    token: str = Depends(reusable_oauth2),
    user_service: UserService = Depends(get_user_service),
) -> User:
    try:
        payload = jwt.decode(
            token, settings.secret_key, algorithms=[settings.algorithm]
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user: User = await user_service.get_user(int(payload["sub"]))
    return user

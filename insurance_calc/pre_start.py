from typing import Any

import aiofiles
import orjson
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from insurance_calc.db.models.user import User
from insurance_calc.settings import settings
from insurance_calc.web.api.auth.service import UserService
from insurance_calc.web.api.insurance.service import InsuranceService


async def db_deploy() -> None:
    async with aiofiles.open("seed.json", "rb") as f:
        data: dict[str, Any] = orjson.loads(await f.read())

    engine = create_async_engine(str(settings.db_url), echo=True)
    async_session_maker = async_sessionmaker(engine, class_=AsyncSession)

    async with async_session_maker() as session:
        user_service: UserService = UserService(session)
        insurance_service: InsuranceService = InsuranceService(session)

        await populate_role(data, user_service)
        await populate_default_user(user_service)
        await populate_insurance(data, insurance_service)


async def populate_default_user(user_service: UserService) -> None:
    user: User | None = await user_service.get_user_by_username(
        username=settings.admin_email
    )
    if not user:
        await user_service.create_user(
            username=settings.admin_email,
            password=settings.admin_password,
            role="Admin",
            is_active=True,
        )


async def populate_role(data: dict[str, Any], user_service: UserService) -> None:
    for role_data in data.get("Role", []):
        await user_service.upsert_role(**role_data)


async def populate_insurance(
    data: dict[str, Any], insurance_service: InsuranceService
) -> None:
    # Insurance seed structure is used as according to the TZ
    for date, insurance_data in data.get("Insurance", {}).items():
        for insurance_data_chunk in insurance_data:
            insurance_data = {**insurance_data_chunk, "date": date}
            await insurance_service.upsert_insurance(**insurance_data)

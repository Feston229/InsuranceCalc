from fastapi import Depends
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from insurance_calc.db.dependencies import get_db_session
from insurance_calc.db.models.insurance import Insurance
from insurance_calc.utils.common import filter_payload
from insurance_calc.web.api.base import BaseService
from insurance_calc.web.api.insurance.schema import (
    CalculationPayload,
    DeleteInsurancePayload,
    QueryInsurancePayload,
    UpdateInsurancePayload,
    UploadInsurancePayload,
)


class InsuranceService(BaseService):
    """Service class for handling insurance-related operations"""

    async def query_insurance(self, payload: QueryInsurancePayload) -> list[Insurance]:
        """Query insurance based on payload"""

        query = select(Insurance).filter_by(**filter_payload(payload))
        insurance_list = await self.session.execute(query)
        insurance_list: list[Insurance] = insurance_list.scalars().all()

        return insurance_list

    async def get_insurance(self, id: int) -> Insurance | None:
        """Get insurance for a given cargo type and date"""

        query = select(Insurance).where(Insurance.id == id)

        insurance = await self.session.execute(query)
        insurance: Insurance = insurance.scalar_one_or_none()

        if not insurance:
            raise ValueError("Insurance not found")

        return insurance

    async def calculate_insurance(self, payload: CalculationPayload) -> float:
        """Calculate insurance based on cargo type and date"""

        insurance: Insurance = await self.get_insurance(payload.id)

        return payload.price * insurance.rate

    async def update_insurance(self, payload: UpdateInsurancePayload) -> Insurance:
        """Update insurance for a given cargo type and date"""

        insurance = await self.get_insurance(payload.id)
        insurance.rate = payload.new_rate

        self.session.add(insurance)
        await self.session.commit()

        return insurance

    async def delete_insurance(self, payload: DeleteInsurancePayload) -> None:
        """Delete insurance for a given cargo type and date"""

        query = delete(Insurance).where(Insurance.id == payload.id)

        await self.session.execute(query)

    async def upsert_insurance(
        self, date: str, cargo_type: str, rate: float
    ) -> Insurance:
        """Upsert insurance for a given cargo type and date"""

        query = select(Insurance).filter_by(date=date, cargo_type=cargo_type, rate=rate)
        insurance = await self.session.execute(query)
        insurance = insurance.scalar_one_or_none()

        if not insurance:
            insurance = Insurance(cargo_type=cargo_type, rate=rate, date=date)
            self.session.add(insurance)
            await self.session.commit()

        return insurance

    async def batch_create(self, payload: UploadInsurancePayload) -> list[Insurance]:
        """Batch create insurance records"""

        data_list: list = []
        for date, data in payload.dict().items():
            for data_chunk in data:
                data_list.append({"date": date, **data_chunk})
        insurance_list: list[Insurance] = [Insurance(**item) for item in data_list]
        self.session.add_all(insurance_list)
        await self.session.commit()

        return insurance_list


async def get_insurance_service(
    session: AsyncSession = Depends(get_db_session),
) -> InsuranceService:
    """Get insurance service instance."""

    return InsuranceService(session)

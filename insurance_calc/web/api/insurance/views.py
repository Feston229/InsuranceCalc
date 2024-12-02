from aiokafka import AIOKafkaProducer
from fastapi import APIRouter, Depends

from insurance_calc.db.models.insurance import Insurance
from insurance_calc.db.models.user import User
from insurance_calc.services.kafka.dependencies import get_kafka_producer
from insurance_calc.services.kafka.utils import KafkaTopic, send_batch
from insurance_calc.utils import schema as utils_schema
from insurance_calc.web.api.auth.service import get_current_user
from insurance_calc.web.api.insurance import schema
from insurance_calc.web.api.insurance.service import (
    InsuranceService,
    get_insurance_service,
)

router = APIRouter()


@router.post("/upload_insurance", response_model=list[schema.InsuranceDTO])
async def upload_insurance(
    payload: schema.UploadInsurancePayload,
    user: User = Depends(get_current_user),
    insurance_service: InsuranceService = Depends(get_insurance_service),
    producer: AIOKafkaProducer = Depends(get_kafka_producer),
) -> list[schema.InsuranceDTO]:
    """Endpoint to batch upload an insurance list."""

    insurance_list: list[Insurance] = await insurance_service.batch_create(payload)

    await send_batch(
        producer, KafkaTopic.INSURANCE.value, user.id, "insurance", insurance_list
    )

    return insurance_list


@router.get("/query_insurance", response_model=list[schema.InsuranceDTO])
async def query_insurance(
    payload: schema.QueryInsurancePayload,
    insurance_service: InsuranceService = Depends(get_insurance_service),
) -> list[schema.InsuranceDTO]:
    """Endpoint to query insurance."""

    insurance_list: list[Insurance] = await insurance_service.query_insurance(payload)

    return insurance_list


@router.post("/update_insurance", response_model=schema.InsuranceDTO)
async def update_insurance(
    payload: schema.UpdateInsurancePayload,
    insurance_service: InsuranceService = Depends(get_insurance_service),
    _user: User = Depends(get_current_user),
) -> schema.InsuranceDTO:
    """Endpoint to update insurance."""

    insurance = await insurance_service.update_insurance(payload)

    return insurance


@router.delete("/delete_insurance", response_model=utils_schema.Message)
async def delete_insurance(
    payload: schema.DeleteInsurancePayload,
    insurance_service: InsuranceService = Depends(get_insurance_service),
    _user: User = Depends(get_current_user),
) -> utils_schema.Message:
    """Endpoint to delete insurance."""

    await insurance_service.delete_insurance(payload)

    return utils_schema.Message(message="Insurance deleted successfully")


@router.get("/calculate_insurance", response_model=schema.Calculation)
async def calculate_insurance(
    payload: schema.CalculationPayload,
    insurance_service: InsuranceService = Depends(get_insurance_service),
) -> schema.Calculation:
    """Endpoint to calculate insurance."""

    calculation = await insurance_service.calculate_insurance(payload)

    return schema.Calculation(total=calculation)

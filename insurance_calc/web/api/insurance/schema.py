from datetime import datetime

from pydantic import BaseModel, ConfigDict, RootModel


class QueryInsurancePayload(BaseModel):
    """
    QueryInsurancePayload class to represent an insurance payload.
    """

    id: int = None
    cargo_type: str = None
    rate: float = None
    date: str = None


class UpdateInsurancePayload(BaseModel):
    """
    UpdateInsurancePayload class to represent an update rate payload.
    """

    id: int
    new_rate: float


class RateItem(BaseModel):
    cargo_type: str
    rate: float


UploadInsurancePayload = RootModel[dict[str, list[RateItem]]]


class Calculation(BaseModel):
    """
    Calculation class to represent a calculation.
    """

    total: float


class DeleteInsurancePayload(BaseModel):
    """
    DeleteInsurancePayload class to represent a delete insurance payload.
    """

    id: int


class CalculationPayload(BaseModel):
    """
    CalculationPayload class to represent a calculation payload.
    """

    id: int
    price: float


class InsuranceDTO(BaseModel):
    """
    Insurance class to represent a rate.
    """

    id: int
    cargo_type: str
    rate: float
    date: str
    created_date: datetime

    model_config = ConfigDict(from_attributes=True)

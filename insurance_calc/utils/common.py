from pydantic import BaseModel


def filter_payload(payload: BaseModel):
    """Remove empty values from payload."""

    return {k: v for k, v in payload.dict().items() if v}

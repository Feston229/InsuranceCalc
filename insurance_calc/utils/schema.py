from pydantic import BaseModel


class Message(BaseModel):
    """
    Base model for message responses.
    """

    message: str

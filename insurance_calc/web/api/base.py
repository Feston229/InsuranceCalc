from sqlalchemy.ext.asyncio import AsyncSession


class BaseService:
    """Base service class."""

    def __init__(self, session: AsyncSession):
        self.session = session

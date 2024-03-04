import loguru
from sqlalchemy.ext.asyncio import AsyncSession as SQLAlchemyAsyncSession


class BaseCRUDRepository:
    def __init__(self, async_session: SQLAlchemyAsyncSession):
        loguru.logger.info(f"Initializing BaseCRUDRepository {type(async_session)}")
        self.async_session = async_session

import typing
from loguru import logger

from sqlalchemy.ext.asyncio import (
    AsyncSession as SQLAlchemyAsyncSession,
)

from src.repository.database import async_db


async def get_async_session() -> typing.AsyncGenerator[SQLAlchemyAsyncSession, None]:
    """
    The function creates an async session, yields it, and then closes it.
    """
    logger.info("Creating async session")
    try:
        logger.info("Yielding async session")
        yield async_db.async_session
    except Exception as e:
        logger.error(e)
        await async_db.async_session.rollback()
    finally:
        logger.info("Closing async session")
        await async_db.async_session.close()

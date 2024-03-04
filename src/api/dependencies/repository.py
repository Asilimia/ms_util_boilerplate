import typing

import fastapi
import loguru
from sqlalchemy.ext.asyncio import (
    AsyncSession as SQLAlchemyAsyncSession,
)

from src.api.dependencies.session import get_async_session
from src.repository.crud.base import BaseCRUDRepository


def get_repository(
    repo_type: typing.Type[BaseCRUDRepository],
) -> typing.Callable[[SQLAlchemyAsyncSession], BaseCRUDRepository]:
    """
    The function `get_repository` returns a callable that takes an
    `SQLAlchemyAsyncSession` object and returns an instance of a repository class
    based on the provided `repo_type`.
    
    :param repo_type: The `repo_type` parameter is a type hint that specifies the
    type of the repository object that will be returned. It is expected to be a
    subclass of `BaseCRUDRepository`
    :type repo_type: typing.Type[BaseCRUDRepository]
    :return: The function `get_repository` returns a callable object `_get_repo`,
    which takes an `SQLAlchemyAsyncSession` object as an argument and returns an
    instance of `BaseCRUDRepository`.
    """
    loguru.logger.info("Getting repository object")
    def _get_repo(
        async_session: SQLAlchemyAsyncSession = fastapi.Depends(get_async_session),
    ) -> BaseCRUDRepository:
        loguru.logger.info(f"Yielding repository {type(repo_type)} {type(async_session)}")
        return repo_type(async_session=async_session)

    return _get_repo

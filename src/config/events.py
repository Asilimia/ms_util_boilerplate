import typing

import fastapi
import loguru

from src.repository.events import (
    dispose_db_connection,
    initialize_db_connection, initialize_redis_connection, close_redis_connection,
)


def execute_backend_server_event_handler(
        backend_app: fastapi.FastAPI,
) -> typing.Any:
    """
    The function `execute_backend_server_event_handler` returns an async function
    that launches backend server events and initializes a database connection.
    
    :param backend_app: The `backend_app` parameter is of type `fastapi.FastAPI`. It
    represents the FastAPI application instance that will be used to launch the
    backend server events
    :type backend_app: fastapi.FastAPI
    :return: The function `execute_backend_server_event_handler` returns a coroutine
    function `launch_backend_server_events`.
    """

    async def launch_backend_server_events() -> None:
        await initialize_db_connection(backend_app=backend_app)
        await initialize_redis_connection(backend_app=backend_app)  # Initialize Redis here

    return launch_backend_server_events


def terminate_backend_server_event_handler(
        backend_app: fastapi.FastAPI,
) -> typing.Any:
    """
    The function `terminate_backend_server_event_handler` returns an event handler
    that stops the backend server and disposes the database connection.
    
    :param backend_app: The `backend_app` parameter is of type `fastapi.FastAPI`. It
    represents the FastAPI application instance that is running the backend server
    :type backend_app: fastapi.FastAPI
    :return: The function `stop_backend_server_events` is being returned.
    """

    @loguru.logger.catch
    async def stop_backend_server_events() -> None:
        await dispose_db_connection(backend_app=backend_app)
        await close_redis_connection(backend_app=backend_app)  # Close Redis connection here

    return stop_backend_server_events

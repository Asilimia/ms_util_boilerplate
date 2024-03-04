import json
import os

import fastapi
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from config.logging import configure_logging, LogResponseMiddleware
import envkey

from api.endpoints import router as api_endpoint_router
from config.events import (
    execute_backend_server_event_handler,
    terminate_backend_server_event_handler,
)
from config.manager import settings


def initialize_auth_application() -> fastapi.FastAPI:
    """
    The function initializes an authentication application in Python using FastAPI
    and sets up middleware, event handlers, and routers.
    :return: an instance of the FastAPI application.
    """
    envkey.load(True)

    configure_logging()

    app = fastapi.FastAPI(**settings.set_backend_app_attributes)  # type: ignore
    app.state.settings = settings

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=settings.IS_ALLOWED_CREDENTIALS,
        allow_methods=settings.ALLOWED_METHODS,
        allow_headers=settings.ALLOWED_HEADERS,
    )
    app.add_middleware(LogResponseMiddleware)

    app.add_event_handler(
        "startup",
        execute_backend_server_event_handler(backend_app=app),
    )
    app.add_event_handler(
        "shutdown",
        terminate_backend_server_event_handler(backend_app=app),
    )

    app.include_router(router=api_endpoint_router, prefix=settings.API_PREFIX)

    return app


auth_app: fastapi.FastAPI = initialize_auth_application()

if __name__ == "__main__":
    uvicorn.run(
        app="main:auth_app",
        host=settings.SERVER_HOST,
        port=settings.SERVER_PORT,
        reload=settings.DEBUG,
        workers=settings.SERVER_WORKERS,
        log_level=settings.LOGGING_LEVEL,
    )

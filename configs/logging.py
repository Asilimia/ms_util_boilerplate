import logging
import sys
import time
from logging.handlers import RotatingFileHandler
from fastapi import Depends, HTTPException
from fastapi import FastAPI
from fastapi import Request
from fastapi.openapi.utils import get_openapi
from pydantic import BaseModel, ValidationError, Field
from starlette.middleware.base import BaseHTTPMiddleware


# Logging configuration function
def configure_logging():
    log_level = logging.INFO
    log_format = "%(asctime)s | [%(levelname)s] | %(message)s"
    logging.basicConfig(level=log_level, format=log_format, handlers=[
        RotatingFileHandler("myapp.log", maxBytes=10000, backupCount=10),
        logging.StreamHandler(sys.stdout),
    ])


# Middleware for logging requests
class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time

        # Initialize a list to hold logged parts
        logged_parts = [
            f"method = {request.method}",
            f"url = {request.url}",
            f"x-correlation-id = {request.headers.get('x-correlation-id')}",
            f"initiator = {request.headers.get('initiator')}",
            f"processTime = {process_time:.4f} seconds",
            f"status_code = {response.status_code}"

        ]

        # Iterate over all attributes of request.state and filter by prefix
        prefix = "app_"
        state_variables = vars(request.state)

        for key, value in state_variables.get("_state", {}).items():
            if key.startswith(prefix):
                logged_parts.append(f"{key} = {value}")

        # Join all parts with " | " and log
        logging.info(" | ".join(logged_parts))

        return response


# Function to apply logging configuration and middleware to a FastAPI app
class CustomHeaders(BaseModel):
    x_correlation_id: str = Field(..., alias="x-correlation-id")
    initiator: str


async def validate_headers(request: Request):
    try:
        headers = CustomHeaders(
            x_correlation_id=request.headers.get("x-correlation-id"),
            initiator=request.headers.get("initiator"),
        )
        return headers
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=e.errors())


def configure_app(app: FastAPI):
    configure_logging()
    app.add_middleware(LoggingMiddleware)

    # app.router.dependencies.append(Depends(validate_headers))

    # Include CustomHeaders model in FastAPI schema
    def custom_openapi():
        if app.openapi_schema:
            return app.openapi_schema
        openapi_schema = get_openapi(
            title=app.title,
            version=app.version,
            description=app.description,
            routes=app.routes,
        )
        components = openapi_schema.setdefault("components", {})
        schemas = components.setdefault("schemas", {})
        schemas["CustomHeaders"] = {
            "type": "object",
            "properties": {
                "x-correlation-id": {"type": "string"},
                "initiator": {"type": "string"},
            },
            "required": ["x-correlation-id", "initiator"],
        }

        # Ensure the required structure exists before accessing it
        openapi_schema.setdefault("paths", {})
        openapi_schema["paths"].setdefault("/", {})
        openapi_schema["paths"]["/"].setdefault("get", {})
        openapi_schema["paths"]["/"]["get"].setdefault("parameters", [])

        openapi_schema["paths"]["/"]["get"]["parameters"] = [
            {
                "name": "x-correlation-id",
                "in": "header",
                "required": True,
                "schema": {"type": "string"},
            },
            {
                "name": "initiator",
                "in": "header",
                "required": True,
                "schema": {"type": "string"},
            },
        ]
        app.openapi_schema = openapi_schema
        return app.openapi_schema

    app.openapi = custom_openapi

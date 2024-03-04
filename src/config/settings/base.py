import json
import logging
import os
import pathlib

import decouple
import envkey
import pydantic
from pydantic_settings import BaseSettings

ROOT_DIR: pathlib.Path = pathlib.Path(
    __file__
).parent.parent.parent.parent.parent.resolve()

envkey.load(True)


# The `BackendBaseSettings` class defines various settings for a backend
# application, including server configuration, database settings, authentication
# settings, logging settings, and more.
class BackendBaseSettings(BaseSettings):
    model_config = pydantic.ConfigDict(
        case_sensitive=True,
        env_file=f"{str(ROOT_DIR)}/.env",
        validate_assignment=True,
    )  # type: ignore

    TITLE: str = "Auth Microservice Application"
    VERSION: str = "0.0.1"
    TIMEZONE: str = "UTC"
    DESCRIPTION: str | None = None
    DEBUG: bool = False

    SERVER_HOST: str = os.getenv("BACKEND_SERVER_HOST")  # type: ignore
    SERVER_PORT: int = os.getenv("BACKEND_SERVER_PORT")  # type: ignore
    SERVER_WORKERS: int = os.getenv("BACKEND_SERVER_WORKERS")  # type: ignore
    API_PREFIX: str = "/api/v1"
    DOCS_URL: str = "/docs"
    OPENAPI_URL: str = "/openapi.json"
    REDOC_URL: str = "/redoc"
    OPENAPI_PREFIX: str = ""
    SECRET_KEY :str= os.getenv("SECRET_KEY")  # type: ignore

    DB_POSTGRES_HOST: str = os.getenv("POSTGRES_HOST")  # type: ignore
    DB_MAX_POOL_CON: int = os.getenv("DB_MAX_POOL_CON")  # type: ignore
    DB_POSTGRES_NAME: str = os.getenv("POSTGRES_DB")  # type: ignore
    DB_POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD")  # type: ignore
    DB_POOL_SIZE: int = os.getenv("DB_POOL_SIZE")  # type: ignore
    DB_POOL_OVERFLOW: int = os.getenv("DB_POOL_OVERFLOW")  # type: ignore
    DB_POSTGRES_PORT: int = os.getenv("POSTGRES_PORT")  # type: ignore
    DB_POSTGRES_SCHEMA: str = os.getenv("POSTGRES_SCHEMA")  # type: ignore
    DB_TIMEOUT: int = os.getenv("DB_TIMEOUT")  # type: ignore
    DB_POSTGRES_USERNAME: str = os.getenv("POSTGRES_USERNAME")  # type: ignore

    IS_DB_ECHO_LOG: bool = os.getenv("IS_DB_ECHO_LOG")  # type: ignore
    IS_DB_FORCE_ROLLBACK: bool = os.getenv("IS_DB_FORCE_ROLLBACK")  # type: ignore
    IS_DB_EXPIRE_ON_COMMIT: bool = os.getenv("IS_DB_EXPIRE_ON_COMMIT")  # type: ignore

    API_TOKEN: str = os.getenv("API_TOKEN")  # type: ignore
    AUTH_TOKEN: str = os.getenv("AUTH_TOKEN")  # type: ignore
    JWT_TOKEN_PREFIX: str = os.getenv("JWT_TOKEN_PREFIX")  # type: ignore
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY")  # type: ignore
    JWT_SUBJECT: str = os.getenv("JWT_SUBJECT")  # type: ignore
    JWT_MIN: int = os.getenv("JWT_MIN")  # type: ignore
    JWT_HOUR: int = os.getenv("JWT_HOUR")  # type: ignore
    JWT_DAY: int = os.getenv("JWT_DAY")  # type: ignore
    JWT_ACCESS_TOKEN_EXPIRATION_TIME: int = int(JWT_MIN) * int(JWT_HOUR) * int(JWT_DAY)
    # messaging

    AFRICASTALKING_MESSAGE_USERNAME: str = os.getenv("AFRICASTALKING_MESSAGE_USERNAME")  # type: ignore
    AFRICASTALKING_MESSAGE_KEY: str = os.getenv("AFRICASTALKING_MESSAGE_KEY")  # type: ignore
    AFRICASTALKING_MESSAGE_URL: str = os.getenv("AFRICASTALKING_MESSAGE_URL")  # type: ignore
    AFRICASTALKING_DEFAULT_SENDER_ID: str = os.getenv("AFRICASTALKING_DEFAULT_SENDER_ID")  # type: ignore

    # redis
    REDIS_URL: str = os.getenv("REDIS_URL")  # type: ignore
    REDIS_MIN_POOL_SIZE: int = os.getenv("REDIS_MIN_POOL_SIZE")  # type: ignore
    REDIS_MAX_POOL_SIZE: int = os.getenv("REDIS_MAX_POOL_SIZE")  # type: ignore

    IS_ALLOWED_CREDENTIALS: bool = os.getenv("IS_ALLOWED_CREDENTIALS")  # type: ignore
    ALLOWED_ORIGINS: list[str] = [
        "http://localhost:3000",  # React default port
        "http://0.0.0.0:3000",
        "http://127.0.0.1:3000",  # React docker port
        "http://127.0.0.1:3001",
        "http://localhost:5173",  # Qwik default port
        "http://0.0.0.0:5173",
        "http://127.0.0.1:5173",  # Qwik docker port
        "http://127.0.0.1:5174",
    ]
    ALLOWED_METHODS: list[str] = ["*"]
    ALLOWED_HEADERS: list[str] = ["*"]

    LOGGING_LEVEL: int = logging.INFO
    LOGGERS: tuple[str, str] = ("uvicorn.asgi", "uvicorn.access")

    HASHING_ALGORITHM_LAYER_1: str = os.getenv("HASHING_ALGORITHM_LAYER_1")  # type: ignore
    HASHING_ALGORITHM_LAYER_2: str = os.getenv("HASHING_ALGORITHM_LAYER_2")  # type: ignore
    HASHING_SALT: str = os.getenv("HASHING_SALT")  # type: ignore
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM")  # type: ignore

    @property
    def set_backend_app_attributes(self) -> dict[str, str | bool | None]:
        """
        Set all `FastAPI` class' attributes with the custom values defined in `BackendBaseSettings`.

        """

        # Optionally, you can update the os.environ with the fetched configuration
        # This step makes EnvKey's fetched variables directly accessible via os.environ
        return {
            "title": self.TITLE,
            "version": self.VERSION,
            "debug": self.DEBUG,
            "description": self.DESCRIPTION,
            "docs_url": self.DOCS_URL,
            "openapi_url": self.OPENAPI_URL,
            "redoc_url": self.REDOC_URL,
            "openapi_prefix": self.OPENAPI_PREFIX,
            "api_prefix": self.API_PREFIX,
        }

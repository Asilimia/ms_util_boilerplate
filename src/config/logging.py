import logging
import sys
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
import os

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from src.securities.hashing.vault import decrypt_data, encrypt_data


def configure_logging():
    """
    Sets up logging configurations to log messages to different files and the console
    with specified formats and settings, using Python's built-in logging module.
    """

    # Create logs directory if it doesn't exist
    if not os.path.exists('logs'):
        os.makedirs('logs')

    # Define log formats
    plain_log_format = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | PID:%(process)d | TID:%(thread)d | %(name)s | %(funcName)s:%(lineno)d - %(message)s",
        "%Y-%m-%d %H:%M:%S")

    # Configure root logger
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)  # Set to lowest level to capture all messages

    # File handler for app.log
    app_file_handler = TimedRotatingFileHandler('logs/app.log', when="midnight", interval=1, backupCount=10)
    app_file_handler.setFormatter(plain_log_format)
    app_file_handler.setLevel(logging.INFO)  # Only log INFO and above to the app.log
    app_file_handler.suffix = "%Y-%m-%d"
    logger.addHandler(app_file_handler)

    # File handler for error.log
    error_file_handler = TimedRotatingFileHandler('logs/error.log', when="midnight", interval=1, backupCount=5)
    error_file_handler.setFormatter(plain_log_format)
    error_file_handler.setLevel(logging.ERROR)  # Only log ERROR and above to the error.log
    error_file_handler.suffix = "%Y-%m-%d"
    logger.addHandler(error_file_handler)

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)  # Change to TRACE equivalent in logging, which is DEBUG
    console_handler.setFormatter(plain_log_format)
    logger.addHandler(console_handler)


class CryptoMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Decrypt request body if it's not empty
        body = await request.body()
        if body:
            decrypted_body = decrypt_data(body)
            # Replace request body with decrypted data
            request._body = decrypted_body

        response = await call_next(request)

        # Encrypt response data
        if response.body:
            encrypted_data = encrypt_data(response.body)
            # Create a new response with encrypted data
            response = Response(content=encrypted_data, media_type="application/octet-stream")

        return response


# logging middleware to log responses to the console and files
class LogResponseMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        # Log the request path, method, and response status code
        # get phone number from  jwt token if it exists also the response body

        logging.info(f"Path={request.url.path}|Method={request.method}|Response Code={response.status_code}")
        return response

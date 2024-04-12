# @app.middleware("http")
from cryptography import fernet
from cryptography.fernet import Fernet
from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request


def configure_login(app: FastAPI, encryption_key: bytes):
    fernet = Fernet(encryption_key)

    class EncryptDecryptMiddleware(BaseHTTPMiddleware):
        async def dispatch(self, request: Request, call_next):
            # Check if the request body is encrypted
            try:
                decrypted_body = fernet.decrypt(await request.body()).decode()
                request._body = decrypted_body.encode()
            except Exception:
                # If decryption fails, assume the request body is not encrypted
                pass

            # Process the request and get the response
            response = await call_next(request)

            # Encrypt the response body
            encrypted_body = fernet.encrypt(response.body)
            response.body = encrypted_body

            return response

    app.add_middleware(EncryptDecryptMiddleware)

# @app.middleware("http")
from cryptography import fernet
from starlette.requests import Request


async def encrypt_decrypt_middleware(request: Request, call_next):
    # Decrypt the request body
    decrypted_body = fernet.decrypt(await request.body()).decode()
    request._body = decrypted_body.encode()

    # Process the request and get the response
    response = await call_next(request)

    # Encrypt the response body
    encrypted_body = fernet.encrypt(response.body)
    response.body = encrypted_body

    return response
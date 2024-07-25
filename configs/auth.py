# auth.py
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import BaseModel
from starlette.requests import Request
import datetime

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")  # Adjust this URL as needed

# JWT configuration
JWT_SECRET_KEY = "8f4f5b0f9a1d3c2e7b6a9d0c3f2e5a8b"
JWT_ALGORITHM = "HS256"  # Typically HS256 is used with secret keys
JWT_SUBJECT = "api_user_authentication"


class UnauthorizedException(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=401, detail=detail)


class DecodedToken(BaseModel):
    sub: str
    username: str
    exp: datetime.datetime
    # Add other relevant claims as needed


def validate_jwt(token: str) -> bool:
    try:
        payload = jwt.decode(
            token,
            JWT_SECRET_KEY,
            algorithms=[JWT_ALGORITHM],
            options={"verify_sub": True}
        )
        if payload["sub"] != JWT_SUBJECT:
            return False
        return True
    except JWTError:
        return False


def get_jwt_payload(token: str) -> dict:
    try:
        payload = jwt.decode(
            token,
            JWT_SECRET_KEY,
            algorithms=[JWT_ALGORITHM],
            options={"verify_sub": True}
        )
        return payload
    except JWTError as token_decode_error:
        raise ValueError("Unable to decode JWT Token") from token_decode_error


async def get_current_user(token: str = Depends(oauth2_scheme)):

    if not validate_jwt(token):
        raise UnauthorizedException("Invalid token")

    try:
        payload = get_jwt_payload(token)
        user = DecodedToken(**payload)
        return user
    except ValueError as e:
        raise UnauthorizedException(str(e))


def auth_required(endpoint):
    async def wrapper(request: Request, current_user: DecodedToken = Depends(get_current_user)):
        return await endpoint(request, current_user=current_user)

    return wrapper


# # Function to generate JWT token (for reference, typically used in your authentication service)
# def generate_access_token(account: dict, expires_delta: datetime.timedelta = None):
#     to_encode = account.copy()
#     if expires_delta:
#         expire = datetime.datetime.utcnow() + expires_delta
#     else:
#         expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
#     to_encode.update({"exp": expire, "sub": JWT_SUBJECT})
#     encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
#     return f"{JWT_TOKEN_PREFIX} {encoded_jwt}"
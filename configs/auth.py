# auth.py
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import BaseModel
from starlette.requests import Request

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="https://13.247.59.145:8443/realms/leja-v3/protocol/openid-connect/token")

# Keycloak configuration
KEYCLOAK_PUBLIC_KEY = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAnM3M1Z/xC3jZg3M+Do5a4M2jsxvw/Oz3fAQ5J2QbwKUSUFPff04q9ErYAs8zmR6hqzkfzZrODHHu5NgkhijrJnnDLN7+y4v+jFlYoe2ZFaFeOlpFHMkAldd3wdWXUD/2AnYeNNWzIm0ZQzgXpnh3cnKwxomd+xGuj2dqupiM8cO9BXqzV83+ebZyCh+iwyUcTw80qcpQUzwoZZcAm2XHYFlVBXSOlzKKAcmeM/7OdxTS88p5Iks8f83T4KZwJM9Z+7nS+vPXTIWxn1wSt1OT/z8L8+gnFPmMPkDfIrgM3XMIJYYgemqTnB2Ph+P3cH5I24PnxHCM7+1bxOdpW+bx4QIDAQAB
-----END PUBLIC KEY-----"""
KEYCLOAK_ALGORITHM = "RS256"
KEYCLOAK_AUDIENCE = "account"
KEYCLOAK_ISSUER = "https://13.247.59.145:8443/realms/leja-v3"


# Custom exception for unauthorized access
class UnauthorizedException(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=401, detail=detail)


# Pydantic model for the decoded token
class DecodedToken(BaseModel):
    sub: str
    name: str
    email: str
    # phone: str

    # Add other relevant claims as needed


# Dependency to decode and validate the access token
async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(
            token,
            KEYCLOAK_PUBLIC_KEY,
            algorithms=[KEYCLOAK_ALGORITHM],
            audience=None,  # Set audience to None to skip audience validation
            issuer=KEYCLOAK_ISSUER,
            options={"verify_aud": False},  # Disable audience validation
        )
        # Get the list of audiences from the token payload
        audiences = payload.get("aud", [])

        # Validate if the token has the expected audience
        if KEYCLOAK_AUDIENCE not in audiences:
            raise JWTError("Invalid audience")

        user = DecodedToken(**payload)
        return user
    except JWTError as e:
        print("Error:", e)
        raise UnauthorizedException("Invalid token")


def auth_required(endpoint):
    async def wrapper(request: Request, current_user: DecodedToken = Depends(get_current_user)):
        return await endpoint(request, current_user=current_user)

    return wrapper

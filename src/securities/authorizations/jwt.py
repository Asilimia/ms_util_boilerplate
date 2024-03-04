import datetime
from typing import Dict

import pydantic
from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt as jose_jwt, JWTError as JoseJWTError

from src.config.manager import settings
from src.models.db.account import Account
from src.models.schemas.jwt import JWTAccount, JWToken
from src.utilities.exceptions.database import EntityDoesNotExist


class JWTGenerator:
    def __init__(self):
        pass

    def _generate_jwt_token(
            self,
            *,
            jwt_data: dict[str, str],
            expires_delta: datetime.timedelta | None = None,
    ) -> str:
        """
        The function `_generate_jwt_token` generates a JSON Web Token (JWT) using
        the provided JWT data and expiration time.
        
        :param jwt_data: The `jwt_data` parameter is a dictionary that contains the
        data to be encoded in the JWT token. It typically includes information such
        as the user's ID, username, or any other relevant data that needs to be
        included in the token
        :type jwt_data: dict[str, str]
        :param expires_delta: The `expires_delta` parameter is an optional parameter
        that specifies the duration for which the JWT token will be valid. It is of
        type `datetime.timedelta` and represents a duration of time. If
        `expires_delta` is provided, the token will expire after the specified
        duration. If `expires_delta`
        :type expires_delta: datetime.timedelta | None
        :return: a JWT (JSON Web Token) as a string.
        """
        to_encode = jwt_data.copy()

        if expires_delta:
            expire = datetime.datetime.now(datetime.timezone.utc) + expires_delta

        else:
            expire = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(
                minutes=settings.JWT_MIN
            )

        to_encode |= JWToken(exp=expire, sub=settings.JWT_SUBJECT).model_dump()

        return jose_jwt.encode(
            to_encode,
            key=settings.JWT_SECRET_KEY,
            algorithm=settings.JWT_ALGORITHM,
        )

    def generate_access_token(self, account: Account) -> str:
        """
        The function generates a JWT access token for a given account.
        
        :param account: The `account` parameter is an instance of the `Account`
        class. It represents the user account for which the access token is being
        generated
        :type account: Account
        :return: a string, which is the generated JWT token.
        """
        if not account:
            raise EntityDoesNotExist(
                "Cannot generate JWT token for without Account entity!"
            )

        return self._generate_jwt_token(
            jwt_data=JWTAccount(username=account.username).model_dump(),  # type: ignore
            expires_delta=datetime.timedelta(
                minutes=settings.JWT_ACCESS_TOKEN_EXPIRATION_TIME
            ),
        )

    def retrieve_details_from_token(self, token: str, secret_key: str) -> list[str]:
        """
        The function `retrieve_details_from_token` decodes a JWT token using a
        secret key, extracts the username from the payload, and returns a list
        containing the username.
        
        :param token: The `token` parameter is a string that represents a JSON Web
        Token (JWT). It is used to authenticate and authorize a user
        :type token: str
        :param secret_key: The `secret_key` parameter is a string that represents
        the secret key used to decode the JWT token. This key should be kept secure
        and should only be known by the server that generates and verifies the JWT
        tokens
        :type secret_key: str
        :return: a list containing the username extracted from the token.
        """
        try:
            payload = jose_jwt.decode(
                token=token, key=secret_key, algorithms=[settings.JWT_ALGORITHM]
            )
            jwt_account = JWTAccount(
                username=payload["username"],
            )

        except JoseJWTError as token_decode_error:
            raise ValueError("Unable to decode JWT Token") from token_decode_error

        except pydantic.ValidationError as validation_error:
            raise ValueError("Invalid payload in token") from validation_error

        return [
            jwt_account.username,
        ]


def get_jwt_payload(authorization: HTTPAuthorizationCredentials = Security(HTTPBearer())) -> Dict[str, str]:
    """
    The function `get_jwt_payload` decodes a JWT token using a secret key and
    returns the payload as a dictionary.

    :param authorization:

    """
    token = authorization.credentials
    if not token:
        raise HTTPException(status_code=403, detail="Invalid authorization credentials.")

    if authorization.scheme.lower() != "bearer":
        raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
    if not authorization.credentials:
        raise HTTPException(status_code=403, detail="Invalid authorization credentials.")

    try:

        payload = jose_jwt.decode(
            token=token, key=settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
        return payload

    except JoseJWTError as token_decode_error:
        raise ValueError("Unable to decode JWT Token") from token_decode_error


def validate_jwt(self, token: str, secret_key: str) -> bool:
    """
    Validates the JWT's signature, expiration, issuer, and audience.

    Args:
        token (str): The JWT to validate.
        secret_key (str): The secret key used to sign the JWT.

    Returns:
        bool: True if the JWT is valid, False otherwise.
    """
    try:
        # Decode the token. This will automatically verify the signature and the exp claim.
        payload = jose_jwt.decode(
            token=token, key=secret_key, algorithms=[settings.JWT_ALGORITHM]
        )

        # If you want to verify the issuer and audience, do so here.
        # For example:
        # if payload["iss"] != expected_issuer:
        #     return False
        # if payload["aud"] != expected_audience:
        #     return False

    except JoseJWTError:
        # Signature verification failed or token has expired
        return False

    # If we've reached this point, the JWT is valid.
    return True


def get_jwt_generator() -> JWTGenerator:
    return JWTGenerator()


jwt_generator: JWTGenerator = get_jwt_generator()

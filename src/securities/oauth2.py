import loguru
from src.config.manager import settings
from src.securities.authorizations.jwt import JWTGenerator, jwt_generator
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/token")


def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    The function `get_current_user` retrieves the username from a JWT token and
    returns it as a dictionary.
    
    :param token: The `token` parameter is a string that represents the
    authentication token provided by the client. It is used to authenticate and
    authorize the user making the request
    :type token: str
    :return: a dictionary with a single key-value pair, where the key is "username"
    and the value is the username retrieved from the token.
    """
    loguru.logger.info(f"get_current_user {token}")
    valid = jwt_generator.validate_jwt(token=token, secret_key=settings.JWT_SECRET_KEY)
    if not valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    username = jwt_generator.retrieve_details_from_token(token, settings.JWT_SECRET_KEY)
    return {"username": username}

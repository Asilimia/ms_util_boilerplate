"""
The HyperText Transfer Protocol (HTTP) 400 Bad Request response status code indicates that the server
cannot or will not process the request due to something that is perceivedto be a client error
(for example, malformed request syntax, invalid request message framing, or deceptive request routing).
"""

import fastapi

from src.utilities.messages.exceptions.http.exc_details import (
    http_400_email_details,
    http_400_signin_credentials_details,
    http_400_signup_credentials_details,
    http_400_username_details,
)


def http_exc_400_credentials_bad_signup_request() -> Exception:
    """
    The function returns an HTTPException with a status code of 400 (Bad Request)
    and a detail message for a signup request with bad credentials.
    :return: An instance of the `fastapi.HTTPException` class is being returned.
    """
    return fastapi.HTTPException(
        status_code=fastapi.status.HTTP_400_BAD_REQUEST,
        detail=http_400_signup_credentials_details(),
    )


def http_exc_400_credentials_bad_signin_request() -> Exception:
    """
    The function returns an HTTPException with a status code of 400 and a detail
    message for bad sign-in credentials.
    :return: an instance of the `fastapi.HTTPException` class.
    """
    return fastapi.HTTPException(
        status_code=fastapi.status.HTTP_400_BAD_REQUEST,
        detail=http_400_signin_credentials_details(),
    )


def http_400_exc_bad_username_request(username: str) -> Exception:
    """
    The function returns a HTTPException with a status code of 400 (Bad Request) and
    a detail message for a request with a bad username.

    :param username: The `username` parameter is a string that represents the
    username for which the HTTP 400 exception is being raised
    :type username: str
    :return: a `fastapi.HTTPException` object.
    """
    return fastapi.HTTPException(
        status_code=fastapi.status.HTTP_400_BAD_REQUEST,
        detail=http_400_username_details(username=username),
    )


def http_400_exc_bad_email_request(email: str) -> Exception:
    """
    The function returns a HTTPException with a status code of 400 (Bad Request) and
    a detail message generated by the http_400_email_details function.

    :param email: The `email` parameter is a string that represents the email
    address that caused the bad request
    :type email: str
    :return: an instance of the `fastapi.HTTPException` class.
    """
    return fastapi.HTTPException(
        status_code=fastapi.status.HTTP_400_BAD_REQUEST,
        detail=http_400_email_details(email=email),
    )

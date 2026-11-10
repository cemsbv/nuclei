import logging
import os
import re

import jwt
import requests
from typing_extensions import deprecated

_NEW_TOKEN_MSG = (
    "Please create a new Nuclei Access Token at "
    "https://nuclei.cemsbv.io/admin/access-token."
)
_LEGACY_NEW_TOKEN_MSG = (
    "The provided token is a Legacy JWT, which is deprecated. "
    f"{_NEW_TOKEN_MSG} "
    "If you still need a Legacy Token for some reason, please contact the CEMS "
    "helpdesk (info@cemsbv.nl)."
)
_REASON_INVALID_ACCESS_TOKEN_MSG = "Your provided Nuclei Access Token is invalid."
_REASON_INVALID_JWT_MSG = "Your provided Legacy JWT is invalid."
_REASON_EXPIRED_JWT_MSG = "Your Legacy JWT has expired."


def create_session() -> requests.Session:
    """
    Initialising session object to call the NUCLEI endpoints.
    Provide the Nuclei Access Token from https://nuclei.cemsbv.io/admin/access-token
    upon request or set it as environment variable "NUCLEI_TOKEN".

    Returns
    -------
    Session
    """

    # initialising session
    _session = requests.Session()

    # set bearer token
    _session.headers.update({"Authorization": f"Bearer {get_valid_user_token()}"})

    return _session


def get_valid_user_token() -> str:
    """
    Obtains the Nuclei Access Token from the env-var "NUCLEI_TOKEN" or prompts the
    user for it, validates it and returns it.
    A prompted token is stored as env-var "NUCLEI_TOKEN" after validation, as a
    side-effect.

    Returns
    -------
    str
        The validated Nuclei Access Token (or Legacy JWT).

    Raises
    ------
    ValueError
        When a Nuclei Access Token does not match the required format.
    jwt.ExpiredSignatureError
        When a Legacy JWT has expired.
    jwt.InvalidTokenError
        When a Legacy JWT cannot be decoded.
    """

    # check if Nuclei Access Token is in environment variables
    if "NUCLEI_TOKEN" in os.environ:
        logging.info("Nuclei Access Token found in environment")
        token = os.environ["NUCLEI_TOKEN"]
        validate_token(token)

    # ask user for Nuclei Access Token
    else:
        token = input(
            "Authentication is needed! Please provide your Nuclei Access Token. "
            "You can obtain your Nuclei Access Token on "
            "https://nuclei.cemsbv.io/admin/access-token."
        )
        validate_token(token)

        os.environ["NUCLEI_TOKEN"] = token
        logging.info("Nuclei Access Token set in environment")

    return token


def validate_token(token: str) -> None:
    """Validate a Nuclei Access Token or Legacy JWT.

    A Legacy JWT (three dot-separated segments) is validated with
    `validate_jwt_token`; any other token with `validate_nuclei_access_token`.

    Parameters
    ----------
    token: str
        The Nuclei Access Token or Legacy JWT.

    Raises
    ------
    ValueError
        When a Nuclei Access Token does not match the required format.
    jwt.ExpiredSignatureError
        When a Legacy JWT has expired.
    jwt.InvalidTokenError
        When a Legacy JWT cannot be decoded.
    """
    if token.count(".") == 2:
        validate_jwt_token(token)
    else:
        validate_nuclei_access_token(token)


def validate_nuclei_access_token(token: str) -> None:
    """Validate the format of a Nuclei Access Token.

    The token must be exactly 21 characters long and consist only of the
    characters "A-Za-z0-9-_".

    Parameters
    ----------
    token: str
        The Nuclei Access Token.

    Raises
    ------
    ValueError
        When the token does not match the required format.
    """
    if not re.fullmatch(r"[A-Za-z0-9_-]{21}", token):
        raise ValueError(f"{_REASON_INVALID_ACCESS_TOKEN_MSG} {_NEW_TOKEN_MSG}")


@deprecated(
    "Legacy JWTs have been deprecated in favor of Nuclei Access Tokens and will "
    "no longer be accepted in a future release.",
    category=FutureWarning,
)
def validate_jwt_token(token: str) -> None:
    """Validate a Legacy JWT by trying to decode it.

    .. deprecated:: 3.3.0
        Legacy JWTs are replaced by Nuclei Access Tokens, see
        `validate_nuclei_access_token`.

    Only the format and expiry are checked; the signature is deliberately not
    verified.

    Parameters
    ----------
    token: str
        The Legacy JWT.

    Raises
    ------
    jwt.ExpiredSignatureError
        When the JWT has expired.
    jwt.InvalidTokenError
        When the JWT cannot be decoded.
    """

    try:
        _ = jwt.decode(
            token,
            algorithms=["HS256"],
            options={"verify_signature": False, "verify_exp": True},
        )
    except jwt.ExpiredSignatureError as e:
        raise jwt.ExpiredSignatureError(
            f"{_REASON_EXPIRED_JWT_MSG} {_LEGACY_NEW_TOKEN_MSG}"
        ) from e

    except jwt.InvalidTokenError as e:
        raise jwt.InvalidTokenError(
            f"{_REASON_INVALID_JWT_MSG} {_LEGACY_NEW_TOKEN_MSG}"
        ) from e


@deprecated(
    "`authenticate` has been deprecated in favor of `get_valid_user_token` and "
    "will be removed in a future release."
)
def authenticate() -> str:
    """
    Returns a validated Nuclei Access Token.

    .. deprecated:: 3.3.0
        Use `get_valid_user_token` instead.

    Prompt the user for a Nuclei Access Token if it is not stored as an
    environmental variable "NUCLEI_TOKEN". A prompted token will be stored as
    env-var after validation.

    Will throw an exception when the token is invalid, see `validate_token`.
    """

    return get_valid_user_token()

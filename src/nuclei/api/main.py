import logging
import os

import jwt
import requests


def create_session() -> requests.Session:
    """
    Initialising session object to call the NUCLEI endpoints.
    Provide the user token from https://nuclei.cemsbv.io/#/personal-access-tokens to
    upon request or set as environment variable.

    Returns
    -------
    Session
    """

    # initialising session
    _session = requests.Session()

    # set bearer token
    _session.headers.update({"Authorization": f"Bearer {authenticate()}"})

    return _session


def authenticate() -> str:
    """
    Returns a validated JWT token from backend.

    Prompt the user for a user-token if it is not stored as an environmental variable
    "NUCLEI_TOKEN". A prompted user token will be stored as env-var after validation.

    Will throw an exception when authentication fails.
    """

    user_token = _get_valid_user_token()

    return user_token


def _get_valid_user_token() -> str:
    """
    Obtains the user-token from the env-vars or stdin and returns it.
    If the token is valid, it is stored as env-var "NUCLEI_TOKEN" as a side-effect.
    """

    # check if User Token is in environment variables
    if "NUCLEI_TOKEN" in os.environ:
        logging.info("user token found in environment")
        token = os.environ["NUCLEI_TOKEN"]
        _validate_user_token(token)

    # ask user for user token
    else:
        token = input(
            "Authentication is needed! Please provide your NUCLEI User Token. "
            "You can obtain your NUCLEI User Token on https://nuclei.cemsbv.io/#/personal-access-tokens."
        )

        _validate_user_token(token)
        os.environ["NUCLEI_TOKEN"] = token
        logging.info("user token set in environment")

    return token


def _validate_user_token(token: str) -> None:
    """Validate a JWT User-token by trying to decode it.

    Parameters
    ----------
    token: str
        The Nuclei User JWT.
    """

    try:
        _ = jwt.decode(
            token,
            algorithms=["HS256"],
            options={"verify_signature": False, "verify_exp": True},
        )
    except jwt.ExpiredSignatureError:
        raise jwt.ExpiredSignatureError(
            "Your NUCLEI User Token is expired. Please create a new token on "
            "https://nuclei.cemsbv.io/#/personal-access-tokens."
        )

    except jwt.InvalidTokenError as e:
        raise jwt.InvalidTokenError(
            "Your NUCLEI User Token is invalid. Please copy your user token from "
            "https://nuclei.cemsbv.io/#/personal-access-tokens. "
            f"The following error occurred: {e}"
        )

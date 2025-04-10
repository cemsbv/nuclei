import logging
import os

import jwt
import aiohttp


def create_session() -> aiohttp.ClientSession:
    """
    Initialising session object to call the NUCLEI endpoints.
    Provide the user token from https://nuclei.cemsbv.io/#/personal-access-tokens to
    upon request or set as environment variable.

    Returns
    -------
    Session
    """

    # set bearer token
    headers = {"Authorization": f"Bearer {_get_valid_user_token()}"}

    return aiohttp.ClientSession(headers=headers)


def _get_valid_user_token() -> str:
    """
    Obtains the user-token from the env-vars or stdin and returns it.
    If the token is valid, it is stored as env-var "NUCLEI_TOKEN" as a side-effect.
    """

    global USER_TOKEN

    if USER_TOKEN:
        return USER_TOKEN

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

    USER_TOKEN = token

    if USER_TOKEN:
        return USER_TOKEN


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

import logging
import os
from typing import Any

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

    def _response_hook(
        r: requests.Response, *args: Any, **kwargs: Any
    ) -> requests.Response:
        """
        Response hook functions to set as event hook on the session.

        This hook does:
            - Update short-lived access token if needed.

        Parameters
        ----------
        r : Response
        args : Any
        kwargs : Any

        Returns
        -------
        Response
        """
        # send new request after update short-lived access token
        try:
            # decode JWT token
            _ = jwt.decode(
                r.request.headers["Authorization"].split(" ")[1],
                algorithms=["HS256"],
                options={"verify_signature": False, "verify_exp": True},
            )
        except jwt.ExpiredSignatureError:
            logging.info(r.text)

            # get short-lived access token
            logging.info("Update Bearer token")
            token = authenticate()

            # set token to header
            _session.headers.update({"Authorization": f"Bearer {token}"})
            r.request.headers["Authorization"] = _session.headers["Authorization"]  # type: ignore

            return _session.send(r.request, verify=False)
        return r

    # set bearer token
    _session.headers.update({"Authorization": f"Bearer {authenticate()}"})

    # set hook
    _session.hooks["response"].append(_response_hook)
    return _session


def authenticate() -> str:
    """
    Returns a validated short-lived token from backend.

    Promts the user for a user-token if it is not stored as an environmental variable
    "NUCLEI_TOKEN". A prompted user token will be stored as env-var after validation.

    Will throw an exception when authentication fails.
    """

    user_token = _get_valid_user_token()

    return _get_valid_shortlived_token(user_token)


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
    """Validade a JWT User-token by trying to decode it.

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


def _get_valid_shortlived_token(user_token: str) -> str:
    """
    Takes a nuclei user-token and returns a valid nuclei shortlived token.
    Will remove the NUCLEI_TOKEN environmental variable key if no token could be
    obtained with the user-token.
    """

    r = requests.get(
        "https://nuclei.cemsbv.io/v1/shortlived-access-token",
        data=user_token,
    )

    if r.status_code == 400 or r.status_code == 401:
        logging.info("Remove user token from environment")
        _ = os.environ.pop("NUCLEI_TOKEN", None)
        raise Exception("Unauthorized - invalid token")
    elif r.status_code != 200:
        logging.info("Remove user token from environment")
        _ = os.environ.pop("NUCLEI_TOKEN", None)
        raise Exception(
            f"Cannot authorize (status: {r.status_code}, msg: {r.json()['msg']})"
        )

    return r.text

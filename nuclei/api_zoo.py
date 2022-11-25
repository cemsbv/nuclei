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
            - Update shortlived access token if needed.

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
                options={"verify_signature": False},
            )
        except jwt.ExpiredSignatureError:
            logging.info(r.text)

            # get short-lived acces token
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
    Get authentication token from backend

    Returns
    -------
    String
    """
    # check if User Token is in environment variables
    if "NUCLEI_TOKEN" in os.environ:
        logging.info("user token found in environment")
        token = os.environ["NUCLEI_TOKEN"]

    # ask user for user token
    else:
        token = input(
            "Authentication is needed! Please provide your NUCLEI User Token. "
            f"You can obtain your NUCLEI User Token on https://nuclei.cemsbv.io/#/personal-access-tokens."
        )

        logging.info("user token set in environment")
        os.environ["NUCLEI_TOKEN"] = token

    r = requests.get(
        "https://nuclei.cemsbv.io/v1/shortlived-access-token",
        data=token,
    )

    if r.status_code == 401:
        raise Exception("Unauthorized - incorrect token")
    elif r.status_code != 200:
        raise Exception(
            f"Cannot authorize (status: {r.status_code}, msg: {r.json()['msg']})"
        )

    return r.text


if __name__ == "__main__":
    # create session
    session = create_session()

    # call healthcheck endpoint PileCore
    response = session.get(url="https://crux-nuclei.com/api/pilecore/v2/healthcheck")

    # Should be "Service alive"
    print(response.text)

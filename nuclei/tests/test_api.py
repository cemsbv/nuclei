import io
import os

import jwt
import pytest
from conftest import (
    mock_expired_jwt,
    mock_get_shortlived_token_200,
    mock_invalid_jwt,
    mock_valid_jwt,
)
from requests import Request, Response, Session
from requests.hooks import dispatch_hook
from requests.models import PreparedRequest

from nuclei.api import main as api


def test_authenticate_stdin_valid(monkeypatch, mock_get_shortlived_token_200):
    """Tries to authenticate with a valid token through stdin,
    without the NUCLEI_TOKEN environmental variable set."""

    monkeypatch.setattr(os, "environ", {})
    monkeypatch.setattr("sys.stdin", io.StringIO(mock_valid_jwt(key="user_secret")))

    api.authenticate()


def test_authenticate_envvar_valid(monkeypatch, mock_get_shortlived_token_200):
    """Tries to authenticate with a valid NUCLEI_TOKEN environmental variable."""
    monkeypatch.setattr(
        os, "environ", {"NUCLEI_TOKEN": mock_valid_jwt(key="user_secret")}
    )

    api.authenticate()


def test_authenticate_stdin_expired(monkeypatch, mock_get_shortlived_token_200):
    """Tries to authenticate with an expired token through stdin.
    Should raise a jwt.ExpiredSignatureError"""

    monkeypatch.setattr(os, "environ", {})
    monkeypatch.setattr("sys.stdin", io.StringIO(mock_expired_jwt(key="user_secret")))

    with pytest.raises(jwt.ExpiredSignatureError):
        api.authenticate()


def test_authenticate_stdin_invalid(monkeypatch, mock_get_shortlived_token_200):
    """Tries to authenticate with an expired token through stdin.
    Should raise a jwt.InvalidTokenError"""

    monkeypatch.setattr(os, "environ", {})
    monkeypatch.setattr("sys.stdin", io.StringIO(mock_invalid_jwt(key="user_secret")))

    with pytest.raises(jwt.InvalidTokenError):
        api.authenticate()


def test_get_shortlived_token_error_400(monkeypatch, mock_get_shortlived_token_400):
    """Tests if _get_valid_shortlived_token raises an Exception if the
    shortlived-token call returns a 400"""

    with pytest.raises(Exception):
        api._get_valid_shortlived_token("")


def test_get_shortlived_token_error_500(monkeypatch, mock_get_shortlived_token_500):
    """Tests if _get_valid_shortlived_token raises an Exception if the
    shortlived-token call returns a 500"""

    with pytest.raises(Exception):
        api._get_valid_shortlived_token("")


def test_create_session(monkeypatch, mock_get_shortlived_token_200):
    """Tests if a requests.Session is created properly with the correct bearer token."""

    monkeypatch.setattr(
        os, "environ", {"NUCLEI_TOKEN": mock_valid_jwt(key="user_secret")}
    )

    session = api.create_session()

    assert isinstance(session, Session)
    assert session.headers["Authorization"] == f"Bearer {mock_valid_jwt()}"


def test_response_hook_valid_token(monkeypatch, mock_get_shortlived_token_200):
    """Tests the response-hook of the session when the request token was valid."""

    # Set a valid user token for authentication
    monkeypatch.setattr(
        os, "environ", {"NUCLEI_TOKEN": mock_valid_jwt(key="user_secret")}
    )

    # Mock a Response object with a valid shortlived-jwt token in its request
    r_valid = Response()
    r_valid.request = Request(headers={"Authorization": f"Bearer {mock_valid_jwt()}"})

    # Create a session and run its response-hook on the response
    session = api.create_session()
    r_after_hook = dispatch_hook("response", session.hooks, r_valid)

    assert r_after_hook.request.headers["Authorization"] == f"Bearer {mock_valid_jwt()}"


def test_response_hook_expired_token(monkeypatch, mock_get_shortlived_token_200):
    """Tests the response-hook of the session when the request token was expired."""

    # Mock the Session.send call so it returns a valid response
    def mock_session_send(self: Session, r: Request, **kwargs) -> Response:
        # Return a response with a valid shortlived jwt token.
        resp = Response()
        resp.request = PreparedRequest()
        resp.request.headers = {"Authorization": f"Bearer {mock_valid_jwt()}"}  # type: ignore
        return resp

    monkeypatch.setattr("requests.Session.send", mock_session_send)

    # Set a valid user token for authentication
    monkeypatch.setattr(
        os, "environ", {"NUCLEI_TOKEN": mock_valid_jwt(key="user_token")}
    )

    # Mock a Response object with an expired shortlived-jwt token in its request
    r_exp = Response()
    r_exp.request = Request(headers={"Authorization": f"Bearer {mock_expired_jwt()}"})

    # Create a session and run its response-hook on the expired response
    session = api.create_session()
    r_after_hook = dispatch_hook("response", session.hooks, r_exp)

    assert r_after_hook.request.headers["Authorization"] == f"Bearer {mock_valid_jwt()}"

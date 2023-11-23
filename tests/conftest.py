import base64
import json
import os
import uuid

import jwt
import pytest
import requests

from nuclei.client.main import ROUTING as routing

unique_key = str(uuid.uuid4())


def mock_valid_jwt(key: str = "") -> str:
    """valid JWT token."""
    return jwt.encode(
        payload={
            "name": "ALL",
            "expires": 999999999999,
            "unique_key": unique_key,
            "user_id": "auth0|1234567890ABCDEFGH",
            "permissions": [
                "read:users",
            ],
        },
        algorithm="HS256",
        key=key,
    )


def mock_expired_jwt(key: str = "") -> str:
    """Expired JWT token. Generated with https://jwt.io/#encoded-jwt"""
    return jwt.encode(
        payload={
            "expires": 99999999,
            "unique_key": unique_key,
            "user_id": "auth0|1234567890ABCDEFGH",
            "roles": None,
            "exp": 99999999,
            "identity": "auth0|1234567890ABCDEFGH",
            "user_claims": {"allowed_access": "free", "email_verified": None},
        },
        algorithm="HS256",
        key=key,
    )


def mock_invalid_jwt(key: str = "") -> str:
    """Invalid JWT token. Generated with https://jwt.io/#encoded-jwt"""
    return mock_expired_jwt(key=key)[:-2]


@pytest.fixture
def mock_json_response():
    r = requests.Response()
    r.headers = {"Content-Type": "application/json"}
    r.status_code = 200
    r._content = bytes(json.dumps({"message": "Test Confirmed"}), "utf-8")
    return r


@pytest.fixture
def mock_text_response():
    r = requests.Response()
    r.headers = {"Content-Type": "text/"}
    r.status_code = 200
    r._content = b"Some text"
    return r


@pytest.fixture
def mock_serialize_json_bytes_parsing_error(monkeypatch):
    """Raise an arbitrary exception on any nuclei.client.utils.serialize_json_bytes call"""

    def mock_serialize_error(*args):
        raise Exception

    monkeypatch.setattr(
        "nuclei.client.utils.serialize_json_bytes", mock_serialize_error
    )


@pytest.fixture
def test_png():
    with open(
        os.path.join(os.path.dirname(__file__), "images/sample.png"), "rb"
    ) as image:
        data = image.read()
    return data


@pytest.fixture
def mock_png_b64_response(test_png):
    r = requests.Response()
    r.headers = {"Content-Type": "image/png;base64"}
    r.status_code = 200
    r._content = base64.b64encode(test_png)
    return r


@pytest.fixture
def mock_png_response(test_png):
    r = requests.Response()
    r.headers = {"Content-Type": "image/png"}
    r.status_code = 200
    r._content = test_png
    return r


@pytest.fixture
def session_send_post_returns_json(monkeypatch, mock_json_response):
    def mock_session_send(self, request: requests.models.PreparedRequest, **kwargs):
        if request.url == routing["PileCore"] + "/MockPostEndpoint":
            return mock_json_response

        raise ValueError(
            "session.send is mocked for this test. Usage is restricted to a fake url."
        )

    monkeypatch.setattr("requests.sessions.Session.send", mock_session_send)


@pytest.fixture
def session_send_get_returns_json(monkeypatch, mock_json_response):
    def mock_session_send(self, request: requests.models.PreparedRequest, **kwargs):
        if request.url == routing["PileCore"] + "/MockGetEndpoint?somekey=somevalue":
            return mock_json_response

        raise ValueError(
            "session.send is mocked for this test. Usage is restricted to a fake url."
        )

    monkeypatch.setattr("requests.sessions.Session.send", mock_session_send)


@pytest.fixture
def session_send_post_returns_b64_png(monkeypatch, mock_png_b64_response):
    def mock_session_send(self, request: requests.models.PreparedRequest, **kwargs):
        if request.url == routing["PileCore"] + "/MockPostEndpoint":
            return mock_png_b64_response

        raise ValueError(
            "session.send is mocked for this test. Usage is restricted to a fake url."
        )

    monkeypatch.setattr("requests.sessions.Session.send", mock_session_send)


@pytest.fixture
def session_send_post_returns_png(monkeypatch, mock_png_response):
    def mock_session_send(self, request: requests.models.PreparedRequest, **kwargs):
        if request.url == routing["PileCore"] + "/MockPostEndpoint":
            return mock_png_response

        raise ValueError(
            "session.send is mocked for this test. Usage is restricted to a fake url."
        )

    monkeypatch.setattr("requests.sessions.Session.send", mock_session_send)


@pytest.fixture
def session_send_post_returns_text(monkeypatch, mock_text_response):
    def mock_session_send(self, request: requests.models.PreparedRequest, **kwargs):
        if request.url == routing["PileCore"] + "/MockPostEndpoint":
            return mock_text_response

        raise ValueError(
            "session.send is mocked for this test. Usage is restricted to a fake url."
        )

    monkeypatch.setattr("requests.sessions.Session.send", mock_session_send)


@pytest.fixture
def get_app_specification_post(monkeypatch):
    def mock_get_app_specification(self, app: str) -> dict:
        if app == "PileCore":
            return {
                "paths": {
                    "/MockPostEndpoint": {"post": {"description": "Mock Post Endpoint"}}
                }
            }
        raise ValueError(
            "The _get_app_specification is mocked in this test. Usage is restricted to the PileCore app."
        )

    monkeypatch.setattr(
        "nuclei.client.main.NucleiClient._get_app_specification",
        mock_get_app_specification,
    )


@pytest.fixture
def get_app_specification_get(monkeypatch):
    def mock_get_app_specification(self, app: str) -> dict:
        if app == "PileCore":
            return {
                "paths": {
                    "/MockGetEndpoint": {"get": {"description": "Mock Get Endpoint"}},
                }
            }
        raise ValueError(
            "The _get_app_specification is mocked in this test. Usage is restricted to the PileCore app."
        )

    monkeypatch.setattr(
        "nuclei.client.main.NucleiClient._get_app_specification",
        mock_get_app_specification,
    )


@pytest.fixture
def get_app_specification_invalid_method(monkeypatch):
    def mock_get_app_specification(self, app: str) -> dict:
        if app == "PileCore":
            return {
                "paths": {
                    "/MockWeirdEndpoint": {
                        "weird": {"description": "Mock Get Endpoint"}
                    },
                }
            }
        raise ValueError(
            "The _get_app_specification is mocked in this test. Usage is restricted to the PileCore app."
        )

    monkeypatch.setattr(
        "nuclei.client.main.NucleiClient._get_app_specification",
        mock_get_app_specification,
    )


@pytest.fixture
def user_token_envvar(monkeypatch):
    """Mocks the environmental variables with just a valid nuclei user-token set as the
    NUCLEI_TOKEN variable."""

    monkeypatch.setattr(
        os, "environ", {"NUCLEI_TOKEN": mock_valid_jwt(key="user_secret")}
    )


@pytest.fixture
def get_app_specification_version(monkeypatch):
    def mock_get_app_specification(self, app: str) -> dict:
        if app == "PileCore":
            return {
                "info": {
                    "version": "0.1.0-beta.1",
                }
            }
        raise ValueError(
            "The _get_app_specification is mocked in this test. Usage is restricted to the PileCore app."
        )

    monkeypatch.setattr(
        "nuclei.client.main.NucleiClient._get_app_specification",
        mock_get_app_specification,
    )

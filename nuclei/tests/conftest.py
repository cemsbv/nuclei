import os
import sys
import uuid

import jwt
import pytest
import requests
from requests import Response

unique_key = str(uuid.uuid4())


def mock_valid_jwt(key: str = "") -> str:
    """valid JWT token."""
    return jwt.encode(
        payload={
            "expires": 999999999999,
            "unique_key": unique_key,
            "user_id": "auth0|1234567890ABCDEFGH",
            "roles": None,
            "exp": 999999999999,
            "identity": "auth0|1234567890ABCDEFGH",
            "user_claims": {"allowed_access": "free", "email_verified": True},
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
def mock_get_shortlived_token_200(monkeypatch):
    def get_shortlived_token(url, data) -> Response:
        if url == "https://nuclei.cemsbv.io/v1/shortlived-access-token":
            r = Response()
            r.status_code = 200
            r._content = bytes(mock_valid_jwt(), "utf-8")
            return r
        else:
            return requests.get(url, data)

    monkeypatch.setattr("requests.get", get_shortlived_token)


@pytest.fixture
def mock_get_shortlived_token_400(monkeypatch):
    def get_shortlived_token(url, data) -> Response:
        if url == "https://nuclei.cemsbv.io/v1/shortlived-access-token":
            r = Response()
            r.status_code = 400
            return r
        else:
            return requests.get(url, data)

    monkeypatch.setattr("requests.get", get_shortlived_token)


@pytest.fixture
def mock_get_shortlived_token_500(monkeypatch):
    def get_shortlived_token(url, data) -> Response:
        if url == "https://nuclei.cemsbv.io/v1/shortlived-access-token":
            r = Response()
            r.status_code = 500
            r._content = b"{'msg':'Error'}"
            return r
        else:
            return requests.get(url, data)

    monkeypatch.setattr("requests.get", get_shortlived_token)

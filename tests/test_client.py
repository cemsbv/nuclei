import io
import json
import os

import pytest
import requests
from IPython.display import Image

from nuclei.client.main import NucleiClient

from .conftest import mock_valid_jwt


def test_client_env_vars(user_token_envvar):
    """Tests if a NucleiClient can be instantiated with correct token in env-var."""

    client = NucleiClient()

    assert isinstance(client.session, requests.Session)


def test_client_stdin(monkeypatch):
    """Tests if a NucleiClient can be instantiated after passing a token through stdin"""

    monkeypatch.setattr(os, "environ", {})
    monkeypatch.setattr("sys.stdin", io.StringIO(mock_valid_jwt(key="user_secret")))

    client = NucleiClient()

    assert isinstance(client.session, requests.Session)
    assert "NUCLEI_TOKEN" in os.environ.keys()


@pytest.mark.parametrize("app", ["PileCore", "VibraCore", "CPT Core"])
def test_applications_to_endpoints(app, user_token_envvar):
    """Tests correct responses for a single application of four endpoints:
    - get_applications: Is the appname in the list?,
    - get_url: Is an url returned for the appname?,
    - get_endpoints: Is a list of endpoints returned for the response of get_url?
    - get_endpoint_type: Does get_endpoint_type return a correct response for each returned endpoint?
    """

    client = NucleiClient()

    # Test get_applications
    apps = client.applications

    assert app in apps

    # Test get_url
    assert isinstance(client.get_url(app), str)

    # Test get_endpoints. Assumes pulic openapi docs for all APIs.
    endpoints = client.get_endpoints(app)

    for endpoint in endpoints:
        assert isinstance(endpoint, str)
        assert endpoint[0] == r"/"

        endpoint_type = client.get_endpoint_type(app, endpoint)

        assert endpoint_type in ("get", "post")


@pytest.mark.parametrize("app", ["pilecore", "vibracore", "CPTCore"])
def test_get_wrong_url(user_token_envvar, app):
    "Tests if a ValueError is raised after passing an erroneous appname"

    client = NucleiClient()

    with pytest.raises(ValueError) as err:
        client.get_url(app)

    assert str(err.value).startswith(
        "Application not available, please select one of the following valid applications"
    )


def test_get_userclaims(user_token_envvar):
    """Tests if the get_user_claims endpoint returns the correct claims for a free user"""

    client = NucleiClient()

    assert client.user_permissions == ["read:users"]


def test_wrong_endpoint_for_type(user_token_envvar):
    """Tests if a ValueError is raised after calling get_endpoint_type with an
    non-existing endpoint"""

    client = NucleiClient()

    with pytest.raises(ValueError) as err:
        client.get_endpoint_type("PileCore", "/some/invalid/endpoint")

    assert str(err.value).startswith(
        "Endpoint name not valid, please select on of the following valid endpoints"
    )


def test_call_endpoint_post_returns_json(
    user_token_envvar,
    get_app_specification_post,
    session_send_post_returns_json,
):
    """Test `call_endpoint`: Post endpoint usage with dictionary schema"""

    client = NucleiClient()

    response = client.call_endpoint(
        app="PileCore", endpoint="/MockPostEndpoint", schema={"somekey": "somevalue"}
    )

    assert isinstance(response, dict)
    assert response["message"] == "Test Confirmed"


def test_call_endpoint_get_returns_json(
    user_token_envvar,
    get_app_specification_get,
    session_send_get_returns_json,
):
    """Test `call_endpoint`: Get endpoint usage with dictionary schema"""

    client = NucleiClient()

    response = client.call_endpoint(
        app="PileCore", endpoint="/MockGetEndpoint", schema={"somekey": "somevalue"}
    )

    assert isinstance(response, dict)
    assert response["message"] == "Test Confirmed"


def test_call_endpoint_string_schema_returns_json(
    user_token_envvar,
    get_app_specification_post,
    session_send_post_returns_json,
):
    """Test `call_endpoint`: post endpoint usage with string schema"""

    client = NucleiClient()

    response = client.call_endpoint(
        app="PileCore",
        endpoint="/MockPostEndpoint",
        schema=json.dumps({"somekey": "somevalue"}),
    )

    assert isinstance(response, dict)
    assert response["message"] == "Test Confirmed"


def test_call_endpoint_return_response(
    user_token_envvar,
    get_app_specification_post,
    session_send_post_returns_json,
):
    """Test `call_endpoint`: usage with return_response flag"""

    client = NucleiClient()

    response = client.call_endpoint(
        app="PileCore",
        endpoint="/MockPostEndpoint",
        schema={"somekey": "somevalue"},
        return_response=True,
    )

    assert isinstance(response, requests.Response)
    assert response.status_code == 200
    assert response.json()["message"] == "Test Confirmed"


def test_call_endpoint_invalid_method(
    user_token_envvar,
    get_app_specification_invalid_method,
):
    """Test `call_endpoint`: Post endpoint usage with invalid method"""

    client = NucleiClient()

    with pytest.raises(NotImplementedError) as err:
        client.call_endpoint(app="PileCore", endpoint="/MockWeirdEndpoint")

    assert (
        str(err.value)
        == "Not a valid HTTP request methode. Only GET or POST requests are supported. "
        "Use the session attribute to get full control of your request. Provided methode: weird"
    )


def test_call_endpoint_post_returns_png(
    user_token_envvar,
    get_app_specification_post,
    session_send_post_returns_png,
):
    """Test `call_endpoint`: Post endpoint usage with dictionary schema.
    Server response is a byte64 encoded png, which nuclei should decode."""

    client = NucleiClient()

    response = client.call_endpoint(
        app="PileCore", endpoint="/MockPostEndpoint", schema={"somekey": "somevalue"}
    )

    assert isinstance(response, Image)


def test_call_endpoint_post_returns_b64_png(
    user_token_envvar,
    get_app_specification_post,
    session_send_post_returns_b64_png,
):
    """Test `call_endpoint`: Post endpoint usage with dictionary schema
    Server response is a png, which nuclei should pass"""

    client = NucleiClient()

    response = client.call_endpoint(
        app="PileCore", endpoint="/MockPostEndpoint", schema={"somekey": "somevalue"}
    )

    assert isinstance(response, Image)


def test_call_endpoint_post_returns_json_with_parsing_error(
    user_token_envvar,
    get_app_specification_post,
    session_send_post_returns_json,
    mock_serialize_json_bytes_parsing_error,
):
    client = NucleiClient()

    with pytest.raises(Exception):
        client.call_endpoint(
            app="PileCore",
            endpoint="/MockPostEndpoint",
            schema={"somekey": "somevalue"},
        )


def test_call_endpoint_post_returns_text(
    user_token_envvar,
    get_app_specification_post,
    session_send_post_returns_text,
):
    client = NucleiClient()

    response = client.call_endpoint(
        app="PileCore", endpoint="/MockPostEndpoint", schema={"somekey": "somevalue"}
    )

    assert isinstance(response, str)
    assert response == "Some text"


def test_call_endpoint_version(
    user_token_envvar,
    get_app_specification_version,
):
    """Test `get_application_version`"""

    client = NucleiClient()

    assert client.get_application_version(app="PileCore") == "0.1.0-beta.1"

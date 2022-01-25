import base64
import getpass
import os
import time
from functools import lru_cache
from typing import Any, List, Optional, Union

import requests
from IPython.display import Image
from nuclei import utils

ROUTING = {
    app: urls
    for app, urls in utils.create_routing_table().items()
    if app not in ["redis", "gef-model-legacy"]
}
INTERNAL = int(os.environ.get("PRODUCTION", 0))
ACCESS_TOKEN: Optional[str] = None
MAX_RECURSION_COUNT = 10


def get_url(app: str) -> str:
    """
    Get API's url

    Parameters
    ----------
    app : str

    Returns
    -------
    url : str
    """
    return ROUTING[app][INTERNAL]


def get_applications() -> List[str]:
    """
    Get available API's in the Nuclei landscape.

    Returns
    -------
    out : list[str]
        Names of the API's
    """
    return list(ROUTING.keys())


@lru_cache(16)
def get_app_specification(app: str) -> dict:
    return requests.get(get_url(app) + "openapi.json").json()


def get_endpoints(app: str) -> List[str]:
    """
    Get available endpoints of single API.

    Parameters
    ----------
    app : str
        Name of the API.

    Returns
    -------
    out : list[str]
        Endpoint urls.
    """
    return list(get_app_specification(app)["paths"].keys())


def get_endpoint_type(app: str, endpoint: str) -> str:
    """
    Parameters
    ----------
    app
        name of the app
    endpoint
        url of the endpoint.

    Returns
    -------
    "get" | "post"
    """
    return list(get_app_specification(app)["paths"][endpoint].keys())[0]


def resolve_ref(spec: dict, ref: str) -> dict:
    """
    Parameters
    ----------
    spec
        full openapi spec of the app
    ref
        reference to look up

    Returns
    -------
    Part of the schema at the ref
    """
    if not ref.startswith("#/"):
        raise ValueError(f"Invalid OpenAPI ref {ref}")  # pragma: no cover
    path = ref[2:].split("/")
    for p in path:
        if p not in spec:
            raise ValueError(f"Unable to resolve OpenAPI ref {ref}")  # pragma: no cover
        spec = spec[p]
    return spec


def flatten_schema_parameters(spec: dict, schema: dict) -> List[str]:
    """
    Used to extract request body parameters from an openapi spec.
    Handles $ref, allOf, anyOf, and oneOf.

    Parameters
    ----------
    spec
        full openapi spec of the app, used to resolve $ref references
    schema
        schema part of the spec to flatten

    Returns
    -------
    List of properties of the root object of the schema
    """
    if schema.get("type") == "object":
        return list(schema.get("properties", {}).keys())
    if "$ref" in schema:
        return flatten_schema_parameters(spec, resolve_ref(spec, schema["$ref"]))
    for key in ["allOf", "anyOf", "oneOf"]:
        if key in schema:
            return [p for s in schema[key] for p in flatten_schema_parameters(spec, s)]
    if "type" in schema:  # pragma: no cover
        return []
    raise ValueError("Unable to parse OpenAPI spec")  # pragma: no cover


@lru_cache(16)
def get_endpoint_parameters(app: str, endpoint: str, method: str = None) -> List[str]:
    """
    Parameters
    ----------
    app
        name of the app
    endpoint
        url of the endpoint
    method
        http method of the endpoint.

    Returns
    -------
    List of parameter names
    """
    if method is None:
        method = get_endpoint_type(app, endpoint)
    else:
        method = method.lower()
    app_spec = get_app_specification(app)
    spec = app_spec["paths"][endpoint][method]
    if method == "get" or "parameters" in spec:
        return [p["name"] for p in spec.get("parameters", [])]
    else:
        request_body = spec.get("requestBody", {})
        if "$ref" in request_body:
            request_body = resolve_ref(app_spec, request_body["$ref"])
        return flatten_schema_parameters(
            app_spec,
            request_body.get("content", {})
            .get("application/json", {})
            .get("schema", {}),
        )


def call_endpoint(
    app: str,
    endpoint: str,
    schema: Union[dict, str],
    return_response: bool = False,
    get_result: bool = True,
    **kwargs: int,
) -> Any:
    """
    Calls an API in the nuclei landscape.

    Parameters
    ----------
    app : str
        Name of the API. call `get_applications` to obtain a list with all applications.
    endpoint : str
        Name of the API's endpoint. call `get_endpoints` to obtain a list with all applications for a given API.
    schema : dict
        The parameter schema for the API. Take a look at the API documentation.
    return_response : bool
        Return the requests response instead of the parsed data object.
    get_result : bool
        Automatically call the /get-result/ endpoint if we receive a task in PENDING status.

    Returns
    -------
    out : dict
        Parsed API's json response.
    """
    validate_or_refresh_token(ACCESS_TOKEN)

    t = get_endpoint_type(app, endpoint)

    if isinstance(schema, str):
        schema = utils.to_json(schema)

    if (
        get_result
        and "delay" not in schema
        and "delay" in get_endpoint_parameters(app, endpoint, t)
    ):
        schema = dict(delay=True, **schema)

    if t == "get":
        r = requests.get(
            utils.validify_url(get_url(app) + endpoint),
            params=utils.python_types_to_message(schema),
            headers={"Authorization": f"Bearer {ACCESS_TOKEN}"},
        )
    else:
        r = requests.post(
            utils.validify_url(get_url(app) + endpoint),
            json=utils.python_types_to_message(schema),
            headers={"Authorization": f"Bearer {ACCESS_TOKEN}"},
        )

    content_type = r.headers["Content-Type"]
    if (
        get_result
        and content_type == "application/json"
        and "/get-result/" in get_app_specification(app)["paths"]
    ):
        result = r.json()
        if (
            isinstance(result, dict)
            and "id" in result
            and result.get("state") == "PENDING"
        ):
            recursion_count = kwargs.get("recursion_count", 0)
            get_result_schema = {"id": result["id"]}
            timeout = min(10, 2 ** recursion_count)
            if "timeout" in get_endpoint_parameters(app, "/get-result/"):
                time.sleep(0.5)
                get_result_schema["timeout"] = timeout - 0.5
            else:
                time.sleep(timeout)
            return call_endpoint(
                app,
                "/get-result/",
                get_result_schema,
                return_response,
                get_result=recursion_count < MAX_RECURSION_COUNT,
                recursion_count=recursion_count + 1,
            )

    if return_response:
        return r

    if content_type == "image/png;base64":
        return Image(base64.b64decode(r.text))
    elif content_type == "image/png":
        return Image(r.content)
    elif content_type == "application/json":
        result = r.json()
        if "msg" in result:
            if result["msg"] == "Token has expired":
                authenticate()
                return call_endpoint(app, endpoint, schema)

        try:
            python_types = utils.message_to_python_types(result)
        except Exception as e:
            print("Nuclei parsing error", e, result)
            return result
        return python_types
    elif content_type.startswith("text/"):
        return r.text
    return r.content


def authenticate() -> None:
    global ACCESS_TOKEN
    if INTERNAL:
        r = requests.get(
            f"http://{os.environ.get('AUTHENTICATON_SERVER_SERVICE_HOST')}"
            f":{os.environ.get('AUTHENTICATON_SERVER_SERVICE_PORT')}"
            "/get-token"
        )
    else:
        if "NUCLEI_USER" in os.environ and "NUCLEI_PASSWORD" in os.environ:
            username = os.environ["NUCLEI_USER"]
            password = os.environ["NUCLEI_PASSWORD"]
        else:
            username = input("Authentication is needed. What is your nuclei username?")
            password = getpass.getpass("What is your password?")
        r = requests.post(
            "https://crux-nuclei.com/login",
            json={"username": username, "password": password},
        )

    if r.status_code == 401:
        raise Exception("Unauthorized - incorrect username and/or password")
    elif r.status_code != 200:
        raise Exception(f"Cannot authorize (status {r.status_code})")

    ACCESS_TOKEN = r.json()["access_token"]


def validate_or_refresh_token(token: Any) -> int:
    """
    Validates the type and time-stamp of the JWT-string and refreshes the token if necessary.
    Returns an int for testing purposes (1 = token refreshed, 2 = token was valid).
    """
    # type is ok, due to short circuiting
    if (
        (not isinstance(token, str))
        or ("." not in token)
        or (not utils.token_time_valid(token))
    ):
        authenticate()
        return 1
    else:
        return 2

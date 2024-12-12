from __future__ import annotations

import base64
import time
from functools import lru_cache
from typing import Any, List, Literal, Optional, Union

import jwt

from nuclei import create_session

# try import serialize functions
try:
    from IPython.display import Image

    from nuclei.client import utils
except ImportError as e:
    raise ImportError(
        "Could not import one of dependencies [numpy, orjson, ipython]. "
        "You must install nuclei[client] in order to use NucleiClient \n"
        rf"Traceback: {e}"
    )

ROUTING = {
    "PileCore": {
        "v2": "https://crux-nuclei.com/api/pilecore/v2",
        "v3": "https://crux-nuclei.com/api/pilecore/v3",
        "latest": "https://crux-nuclei.com/api/pilecore/v3",
    },
    "VibraCore": {
        "v2": "https://crux-nuclei.com/api/vibracore/v2",
        "latest": "https://crux-nuclei.com/api/vibracore/v2",
    },
    "CPT Core": {
        "v1": "https://crux-nuclei.com/api/cptcore/v1",
        "latest": "https://crux-nuclei.com/api/cptcore/v1",
    },
    "ShallowCore": {
        "v1": "https://crux-nuclei.com/api/shallowcore/v1",
        "latest": "https://crux-nuclei.com/api/shallowcore/v1",
    },
}

DEFAULT_REQUEST_TIMEOUT = 10
MAX_RETRIES = 10


class NucleiClient:
    def __init__(self) -> None:
        """
        NUCLEI Client.

        This class allows the user to interact with our APIs. API documentation can be
        found on our platform > https://nuclei.cemsbv.io/#

        Attributes
        -----------
        session: Session
            requests.Session with authorisation set
        routing: dict
            Routing table to all available API's in the Nuclei landscape.
        timeout: int
            The connect timeout is the number of seconds. Default is 5 seconds
        """

        # initialize session
        self.session = create_session()

        # get routing table to application
        self.routing = ROUTING

        # set default timeout
        self.timeout = DEFAULT_REQUEST_TIMEOUT

    def get_url(self, app: str, version: str = "latest") -> str:
        """
        Get API's url

        Parameters
        ----------
        app: str
            Name of the API. Call `applications` to obtain a list with all applications.
        version: str, optional
            default is latest.
            API version used. Call `get_versions` to obtain a list with all version of a specific application.

        Returns
        -------
        url : str

        Raises
        -------
        TypeError:
            Wrong type for `app` or `version` argument
        ValueError:
            Wrong value for `app` or `version` argument
        """
        if not isinstance(version, str):
            raise TypeError(
                f"Expected positional argument `version` to be of type <class 'str'>, but got type: {type(version)}"
            )
        if version not in self.get_versions(app):
            raise ValueError(
                f"Application version not available, please select one of the following valid versions {self.get_versions(app)}"
            )
        return self.routing[app][version]

    @property
    def user_permissions(self) -> List[str | None]:
        """
        Provide the user permissions of your token.

        Returns
        -------
        out : list[str]
            Names of the API's
        """
        return jwt.decode(
            self.session.headers["Authorization"].split(" ")[1],  # type: ignore
            algorithms=["HS256"],
            options={"verify_signature": False, "verify_exp": False},
        ).get("permissions", [])

    @property
    def applications(self) -> List[str]:
        """
        Provide available API's in the Nuclei landscape.

        Returns
        -------
        out : list[str]
            Names of the API's
        """
        return list(self.routing.keys())

    def get_versions(self, app: str) -> List[str]:
        """
        Provide available API's versions in the Nuclei landscape.

        Parameters
        ----------
        app: str
            Name of the API. Call `applications` to obtain a list with all applications.

        Returns
        -------
        out : list[str]
            Versions of the API.

        Raises
        -------
        TypeError:
            Wrong type for `app` argument
        ValueError:
            Wrong value for `app` argument
        """
        if not isinstance(app, str):
            raise TypeError(
                f"Expected positional argument `app` to be of type <class 'str'>, but got type: {type(app)}"
            )
        if app not in self.applications:
            raise ValueError(
                f"Application not available, please select one of the following valid applications {self.applications}"
            )
        return list(self.routing[app].keys())

    @lru_cache(16)
    def _get_app_specification(self, app: str, version: str = "latest") -> dict:
        """
        Private methode to get the JSON schema of the API documentation.

        Parameters
        ----------
        app: str
            Name of the API. Call `applications` to obtain a list with all applications.
        version: str, optional
            default is latest.
            API version used. Call `get_versions` to obtain a list with all version of a specific application.

        Returns
        -------
        dict

        Raises
        -------
        ConnectionError:
            Application not available
        TypeError:
            Wrong type for `app` or `version` argument
        ValueError:
            Wrong value for `app` or `version` argument
        """
        response = self.session.get(
            self.get_url(app, version) + "/openapi.json", timeout=self.timeout
        )
        if response.status_code != 200:
            raise ConnectionError(
                "Unfortunately the application you are trying to reach is unavailable (status code: "
                f"{response.status_code}). Please check you connection. If the problem persists contact "
                "CEMS at info@cemsbv.nl"
            )
        return response.json()

    def get_application_version(self, app: str, version: str = "latest") -> str:
        """
        Provide the semanctic version of the API in the Nuclei landscape.

        Parameters
        ----------
        app: str
            Name of the API. Call `applications` to obtain a list with all applications.
        version: str, optional
            default is latest.
            API version used. Call `get_versions` to obtain a list with all version of a specific application.

        Returns
        -------
        out : str
            Semantic Version of the API

        Raises
        -------
        ConnectionError:
            Application not available
        TypeError:
            Wrong type for `app` or `version` argument
        ValueError:
            Wrong value for `app` or `version` argument
        """
        return self._get_app_specification(app, version)["info"]["version"]

    def get_endpoints(self, app: str, version: str = "latest") -> List[str]:
        """
        Get available endpoints of single API.

        Parameters
        ----------
        app: str
            Name of the API. Call `applications` to obtain a list with all applications.
        version: str, optional
            default is latest
            API version used. Call `get_versions` to obtain a list with all version of a specific application.

        Returns
        -------
        endpoints : list[str]
            Endpoint urls.

        Raises
        -------
        ConnectionError:
            Application not available
        TypeError:
            Wrong type for `app` or `version` argument
        ValueError:
            Wrong value for `app` or `version` argument
        """
        return list(self._get_app_specification(app, version)["paths"].keys())

    def get_endpoint_type(
        self, app: str, endpoint: str, version: str = "latest"
    ) -> List[str]:
        """
        Get a list of HTTP methods used for this endpoint.

        Parameters
        ----------
        app: str
            Name of the API. Call `applications` to obtain a list with all applications.
        endpoint
            url of the endpoint.
        version: str, optional
            default is latest.
            API version used. Call `get_versions` to obtain a list with all version of a specific application.

        Returns
        -------
        methods: List[str]
            List of HTTP methods used for endpoint

        Raises
        -------
        ConnectionError:
            Application not available
        TypeError:
            Wrong type for an argument
        ValueError:
            Wrong value for an argument
        """
        if not isinstance(endpoint, str):
            raise TypeError(
                f"Expected positional argument `endpoint` to be of type <class 'str'>, but got type: {type(endpoint)}"
            )

        if endpoint in self.get_endpoints(app, version):
            return list(
                self._get_app_specification(app, version)["paths"][endpoint].keys()
            )
        raise ValueError(
            f"Endpoint name not valid, please select on of the following valid endpoints {self.get_endpoints(app, version)}"
        )

    def call_endpoint(
        self,
        app: str,
        endpoint: str,
        methode: Literal["auto", "get", "post"] = "auto",
        version: str = "latest",
        schema: Optional[Union[dict, str]] = None,
        return_response: bool = False,
    ) -> Any:
        """
        Calls an API in the nuclei landscape.

        Note
        --------
        The provided `schema` is serialized by the `utils.serialize_jsonifyable_object`. For get request the
        payload is passed to the `params` parameter of `request.get` function. For post request the payload
        is passed to the `json`  parameter of `request.post` function. This has an effect on the request content type.

        Parameters
        ----------
        app: str
            Name of the API. Call `applications` to obtain a list with all applications.
        endpoint: str
            Name of the API's endpoint. call `get_endpoints` to obtain a list with all applications for a given API.
        methode: str
            default is auto
            HTTP methode used to call endpoint. When auto methode is selected the HTTP methode is
            obtained from the openapi docs. Please note that this is the first one. call `get_endpoint_type`
            to obtain list with all methods related to the endpoint.
        version: str, optional
            default is latest.
            API version used. Call `get_versions` to obtain a list with all versions of a specific application.
        schema: dict or json-string, optional
            Default is None
            The parameter schema for the API. Take a look at the API documentation.
        return_response: bool, optional
            Default is False
            Return the requests response instead of the parsed data object.

        Returns
        -------
        json : dict
            json response
        text : str
            text response
        content : bytes
            content response
        out : Response
            requests response object
        figure: Image
             IPython display Image object

        Raises
        -------
        RuntimeError:
            Thrown when response is between 400 and 600 to see if
            there was a client error or a server error.
        NotImplementedError:
            HTTP methode not get or post request
        ConnectionError:
            Application not available
        TypeError:
            Wrong type for an argument
        ValueError:
            Wrong value for an argument
        """
        if not isinstance(endpoint, str):
            raise TypeError(
                f"Expected positional argument `endpoint` to be of type <class 'str'>, but got type: {type(endpoint)}"
            )

        if endpoint not in self.get_endpoints(app, version):
            raise ValueError(
                f"Endpoint name not valid, please select on of the following valid endpoints {self.get_endpoints(app, version)}"
            )

        if not isinstance(methode, str):
            raise TypeError(
                f"Expected keyword-argument `methode` to be of type <class 'str'>, but got type: {type(methode)}"
            )
        if methode not in ["auto", "get", "post"]:
            raise ValueError(
                f'Expected value of keyword-argument `methode` to be one of ["auto", "get", "post"] , but got: {methode}'
            )

        if not (schema is None or isinstance(schema, (str, dict))):
            raise TypeError(
                f"Expected keyword-argument `schema` to be of type <class 'dict'> or <class 'str'>, but got type: {type(schema)}"
            )

        if not isinstance(return_response, bool):
            raise TypeError(
                f"Expected keyword-argument `return_response` to be of type <class 'bool'>, but got type: {type(return_response)}"
            )

        if methode == "auto":
            t = self.get_endpoint_type(app=app, version=version, endpoint=endpoint)[0]
        else:
            t = methode

        if isinstance(schema, str):
            schema = utils.to_json(schema)

        if t.lower() not in ["get", "post"]:
            raise NotImplementedError(
                "Not a valid HTTP request methode. Only GET or POST requests are supported. "
                f"Use the session attribute to get full control of your request. Provided methode: {t}"
            )

        execution_count = 0

        # We enter a retry-loop for the execution of the main call, with a MAX_RETRIES
        # being the maximum number of retires
        while execution_count < MAX_RETRIES:
            execution_count += 1

            if t.lower() == "get":
                response = self.session.get(
                    self.get_url(app=app, version=version) + endpoint,
                    params=utils.serialize_jsonifyable_object(schema),
                    timeout=self.timeout,
                )
            elif t.lower() == "post":
                response = self.session.post(
                    self.get_url(app=app, version=version) + endpoint,
                    json=utils.serialize_jsonifyable_object(schema),
                    timeout=self.timeout,
                )

            # If the response contains one of the following statuses, retry the request.
            #   429 Too Many Requests
            #   502 Bad Gateway
            #   503 Service Unavailable
            #   504 Gateway Timeout
            status_codes_that_trigger_retry = [429, 502, 503, 504]
            if response.status_code in status_codes_that_trigger_retry:
                # If the call failed, and retry is a viable option, we sleep for a
                # little while and execute another call
                time.sleep(1)
                continue

            # We break the retry loop by default
            break

        if return_response:
            return response

        if not response.ok:
            raise RuntimeError(
                "An error was thrown during your request. Please take a look at the response object for "
                "more information. You can get the response object by setting the `return_response` attribute"
                "to True. \n"
                f"Request URL: {response.url} \n"
                f"Status code: {response.status_code} \n"
                f"Message:     {response.content[:100]!r}"
            )

        content_type = response.headers["Content-Type"]
        if content_type == "image/png;base64":
            return Image(base64.b64decode(response.text))
        elif content_type == "image/png":
            return Image(response.content)
        elif content_type.endswith("json"):
            return response.json()
        elif content_type.startswith("text/"):
            return response.text
        return response.content

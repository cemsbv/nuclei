from __future__ import annotations

import base64
from functools import lru_cache
from typing import Any, List, Literal, Optional, Union

import jwt
import requests

from nuclei import create_session

# try import serialize functions
try:
    from IPython.display import Image

    from nuclei.client import utils
except ImportError as e:
    raise ImportError(
        "Could not import one of dependencies [numpy, ipython]. "
        "You must install nuclei[client] in order to use NucleiClient \n"
        rf"Traceback: {e}"
    )

ROUTING = {
    "PileCore": "https://crux-nuclei.com/api/pilecore/v2",
    "VibraCore": "https://crux-nuclei.com/api/vibracore/v2",
    "CPT Core": "https://crux-nuclei.com/api/cptcore/v1",
    "ShallowCore": "https://crux-nuclei.com/api/shallowcore/v1",
}

DEFAULT_REQUEST_TIMEOUT = 5


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

        """

        # initialize session
        self.session = create_session()

        # get routing table to application
        self.routing = ROUTING

    def get_url(self, app: str) -> str:
        """
        Get API's url

        Parameters
        ----------
        app : str
            Application name

        Returns
        -------
        url : str
        """
        if app in self.applications:
            return self.routing[app]
        raise ValueError(
            f"Application not available, please select one of the following valid applications {self.applications}"
        )

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

    @lru_cache(16)
    def _get_app_specification(self, app: str) -> dict:
        """
        Private methode to get the JSON schema of the API documentation.

        Parameters
        ----------
        app : str
            Name of the API.

        Returns
        -------
        dict
        """
        response = requests.get(
            self.get_url(app) + "/openapi.json", timeout=DEFAULT_REQUEST_TIMEOUT
        )
        if response.status_code != 200:
            raise ConnectionError(
                "Unfortunately the application you are trying to reaches is unavailable (status code: "
                f"{response.status_code}). Please check you connection. If the problem persist contact "
                "CEMS at info@cemsbv.nl"
            )
        return response.json()

    def get_application_version(self, app: str) -> str:
        """
        Provide version of the API in the Nuclei landscape.

        Parameters
        ----------
        app : str
            Name of the API.

        Returns
        -------
        out : str
            Semantic Version of the API
        """
        return self._get_app_specification(app)["info"]["version"]

    def get_endpoints(self, app: str) -> List[str]:
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
        return list(self._get_app_specification(app)["paths"].keys())

    def get_endpoint_type(self, app: str, endpoint: str) -> str:
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

        if endpoint in self.get_endpoints(app):
            return list(self._get_app_specification(app)["paths"][endpoint].keys())[0]
        raise ValueError(
            f"Endpoint name not valid, please select on of the following valid endpoints {self.get_endpoints(app)}"
        )

    def call_endpoint(
        self,
        app: str,
        endpoint: str,
        methode: Literal["auto", "get", "post"] = "auto",
        schema: Optional[Union[dict, str]] = None,
        return_response: bool = False,
    ) -> Any:
        """
        Calls an API in the nuclei landscape.

        Parameters
        ----------
        app: str
            Name of the API. call `get_applications` to obtain a list with all applications.
        endpoint: str
            Name of the API's endpoint. call `get_endpoints` to obtain a list with all applications for a given API.
        methode: str
            default  is auto
            HTTP methode used to call endpoint. When auto methode is selected the HTTP methode is
            obtained from the openapi docs.
        schema: dict, optional
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
        ValueError:
            Endpoint does not exist in the API landscape
        ConnectionError:
            Application not available
        """

        if methode == "auto":
            t = self.get_endpoint_type(app, endpoint)
        else:
            t = methode

        if isinstance(schema, str):
            schema = utils.to_json(schema)

        if t.lower() == "get":
            response = self.session.get(
                self.get_url(app) + endpoint,
                params=utils.serialize_jsonifyable_object(schema),
                timeout=DEFAULT_REQUEST_TIMEOUT,
            )
        elif t.lower() == "post":
            response = self.session.post(
                self.get_url(app) + endpoint,
                json=utils.serialize_json_string(schema),
                timeout=DEFAULT_REQUEST_TIMEOUT,
            )
        else:
            raise NotImplementedError(
                "Not a valid HTTP request methode. Only GET or POST requests are supported. "
                f"Use the session attribute to get full control of your request. Provided methode: {t}"
            )

        if return_response:
            return response

        if not response.ok:
            raise RuntimeError(
                "An error was thrown during your reqeust. Please take a look at the response object for "
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

import base64
from functools import lru_cache
from typing import Any, List, Optional, Union

import requests
from IPython.display import Image
from nuclei import create_session

# try import serialize and deserialize functions
try:
    from nuclei.client import utils
except ImportError:
    utils = None  # type: ignore

# TODO get routing from endpoint
ROUTING = {
    "PileCore": "https://crux-nuclei.com/api/pilecore/v2",
    "VibraCore": "https://crux-nuclei.com/api/vibracore/v1",
    "CPT Core": "https://crux-nuclei.com/api/gef-model",
}


class NucleiClient:
    def __init__(self) -> None:
        """
        NUCLEI Client.

        This class allows the user to interact with our APIs. API documentation can be
        found on our platform > https://nuclei.cemsbv.io/#
        """
        if utils is None:
            raise ImportError(
                "Could not import one of dependencies [geopandas, numpy, pandas, polars].  "
                "Must install nuclei[client] in order to use NucleiClient"
            )

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
        if app in self.get_applications:
            return self.routing[app]
        raise ValueError(
            f"Application not available, please select on of the following valid application {self.routing.keys()}"
        )

    @property
    def get_applications(self) -> List[str]:
        """
        Get available API's in the Nuclei landscape.
        Returns
        -------
        out : list[str]
            Names of the API's
        """
        return list(self.routing.keys())

    @lru_cache(16)
    def get_app_specification(self, app: str) -> dict:
        return requests.get(self.get_url(app) + "/openapi.json").json()

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
        return list(self.get_app_specification(app)["paths"].keys())

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
            return list(self.get_app_specification(app)["paths"][endpoint].keys())[0]
        raise ValueError(
            f"Endpoint name not valid, please select on of the following valid application {self.get_endpoints(app)}"
        )

    def call_endpoint(
        self,
        app: str,
        endpoint: str,
        schema: Optional[Union[dict, str]] = None,
        return_response: bool = False,
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
        Returns
        -------
        out : dict
            Parsed API's json response.
        """

        t = self.get_endpoint_type(app, endpoint)

        if isinstance(schema, str):
            schema = utils.to_json(schema)

        if t == "get":
            r = self.session.get(
                self.get_url(app) + endpoint,
                params=utils.python_types_to_message(schema),
            )
        else:
            r = self.session.post(
                self.get_url(app) + endpoint,
                json=utils.python_types_to_message(schema),
            )

        if return_response:
            return r

        content_type = r.headers["Content-Type"]
        if content_type == "image/png;base64":
            return Image(base64.b64decode(r.text))
        elif content_type == "image/png":
            return Image(r.content)
        elif content_type == "application/json":
            result = r.json()
            try:
                python_types = utils.message_to_python_types(result)
            except Exception as e:
                print("Nuclei parsing error", e, result)
                return result
            return python_types
        elif content_type.startswith("text/"):
            return r.text
        return r.content


if __name__ == "__main__":
    # create session
    client = NucleiClient()

    for appname in ROUTING.keys():
        # call healthcheck endpoint
        response = client.call_endpoint(app=appname, endpoint="/healthcheck")

        # Should be "Service alive"
        print(appname + " - " + str(response))

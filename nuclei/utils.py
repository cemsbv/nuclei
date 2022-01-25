import base64
import binascii
import io
import json
import os
import re
import time
import warnings
from collections.abc import Collection, Mapping
from typing import Any, Dict, Tuple, Type, Union

import numpy as np
import pandas as pd
import polars as pl
import requests

try:
    import geopandas as gpd
except ImportError:
    gpd = None

MSG = (
    "Could not import geopandas.  Must install nuclei[geo] "
    " in order to use validate method"
)

DF = "DataFrame"
DF_PARQUET = "DataFrame.parquet"
PDS = "Series"
NUMPY = "numpy"
GDF = "GeoDataFrame"
GPDS = "GeoSeries"
POLARS_DF = "POLARS_DataFrame"
PANDAS_DF = "PANDAS_DataFrame"
PANDAS_DF_PARQUET = "PANDAS_DataFrame.parquet"
PANDAS_PDS = "PANDAS_Series"


def buffer_to_base64(buf: io.BytesIO) -> str:
    buf.seek(0)
    return base64.b64encode(buf.read()).decode("utf-8")


def base64_to_buffer(blob: bytes) -> io.BytesIO:
    blob = base64.b64decode(blob)
    buf = io.BytesIO()
    buf.write(blob)
    return buf


def deserialize_polars_json(message: dict) -> Union[pd.DataFrame, pd.Series]:
    """
    Only needed for backwards compatibility.
    """
    return pl.read_json(message["body"])


def serialize_polars_json(obj: pl.DataFrame) -> dict:
    return {"nuclei": {"type": POLARS_DF}, "body": obj.to_json()}


def deserialize_pandas_json(message: dict) -> Union[pd.DataFrame, pd.Series]:
    """
    Only needed for backwards compatibility.
    """
    typ = "frame"
    if message["nuclei"]["type"] == PDS or message["nuclei"]["type"] == PANDAS_PDS:
        typ = "series"

    return pd.read_json(message["body"], typ=typ).sort_index()


def serialize_pandas_json(obj: Union[pd.DataFrame, pd.Series]) -> dict:
    if isinstance(obj, pd.DataFrame):
        return {"nuclei": {"type": PANDAS_DF}, "body": obj.to_json()}
    else:
        return {"nuclei": {"type": PANDAS_PDS}, "body": obj.to_json()}


def serialize_pandas_parquet(obj: Union[pd.DataFrame, pd.Series]) -> dict:
    buf = io.BytesIO()
    if isinstance(obj, pd.Series):
        obj = obj.to_frame(obj.name)
    try:
        obj.to_parquet(buf, index=True)
    except Exception:
        return {"nuclei": {"type": PANDAS_DF}, "body": obj.to_json()}

    return {"nuclei": {"type": PANDAS_DF_PARQUET}, "body": buffer_to_base64(buf)}


def deserialize_pandas_parquet(message: dict) -> pd.DataFrame:
    buf = base64_to_buffer(message["body"])
    return pd.read_parquet(buf)


def deserialize_geopandas_json(
    message: dict,
) -> Union[Type["gpd.GeoDataFrame"], Type["gpd.GeoSeries"], Any]:
    """
    Only needed for backwards compatibility.
    """
    if gpd is None:
        raise ImportError(MSG)

    obj = gpd.read_file(message["body"]).reset_index(drop=True)
    obj = obj.drop(columns="id")

    if len(obj.columns) == 1 and obj.columns[0] == "geometry":
        obj = obj.geometry

    return obj


def serialize_geopandas_json(
    obj: Union[Type["gpd.GeoDataFrame"], Type["gpd.GeoSeries"]]
) -> dict:
    if gpd is None:
        raise ImportError(MSG)

    if isinstance(obj, gpd.GeoDataFrame):
        return {"nuclei": {"type": GDF}, "body": obj.to_json()}
    else:
        return {"nuclei": {"type": GPDS}, "body": obj.to_json()}


def serialize_numpy(array: np.ndarray) -> dict:
    buf = io.BytesIO()
    np.save(buf, array, allow_pickle=False)
    return {"nuclei": {"type": NUMPY}, "body": buffer_to_base64(buf)}


def deserialize_numpy(message: dict) -> np.ndarray:
    buf = base64_to_buffer(message["body"])
    buf.seek(0)
    return np.load(buf, allow_pickle=False)


def python_types_to_message(
    schema: Union[
        dict,
        pd.Series,
        pd.DataFrame,
        pl.DataFrame,
        Type["gpd.GeoSeries"],
        Type["gpd.GeoDataFrame"],
        np.ndarray,
        list,
        str,
        float,
        int,
        bool,
    ],
    use_json: bool = True,
) -> Any:
    """
    Cast python types to jsonifyable message.

    Parameters
    ----------
    schema
    use_json
        Added for rollout reasons. Use old json formatting until every backend and the frontend is updated.

    Returns
    -------
    message
        jsonifyable message.
    """
    use_json = not bool(os.environ.get("FORCE_SERIALIZATION", not use_json))
    if gpd is not None:
        if isinstance(schema, (gpd.GeoDataFrame, gpd.GeoSeries)):
            if use_json:
                return serialize_geopandas_json(schema)
            return NotImplemented
    if isinstance(schema, pl.DataFrame):
        if use_json:
            return serialize_polars_json(schema)
        return NotImplemented
    if isinstance(schema, (pd.DataFrame, pd.Series)):
        if use_json:
            return serialize_pandas_json(schema)
        return serialize_pandas_parquet(schema)
    if isinstance(schema, np.ndarray):
        if use_json:
            # no NaN in array
            if not np.isnan(schema).any():
                return schema.tolist()
            else:
                return json.loads(json.dumps(schema.tolist()).replace("NaN", "null"))
        return serialize_numpy(schema)
    # recurse and convert to jsonifyable types
    if isinstance(schema, Mapping):
        return {k: python_types_to_message(v) for k, v in schema.items()}
    if isinstance(schema, Collection) and not isinstance(schema, str):
        return [python_types_to_message(k) for k in schema]
    return schema


def message_to_python_types(
    message: Union[
        dict,
        list,
        str,
        float,
        int,
        bool,
    ]
) -> Union[
    dict,
    pd.Series,
    pd.DataFrame,
    pl.DataFrame,
    Type["gpd.GeoSeries"],
    Type["gpd.GeoDataFrame"],
    np.ndarray,
    list,
    str,
    float,
    int,
    bool,
]:
    """
    Cast json result to python types by searching for objects

    Parameters
    ----------
    message
        parsed json message

    Returns
    -------
    schema
        schema with original python types.
    """

    if isinstance(message, dict):
        # input is a custom serialized type
        if "nuclei" in message and len(message) == 2:
            t = message["nuclei"]["type"]
            if t == DF_PARQUET:
                warnings.warn(
                    "`DataFrame.parquet` is deprecated and will soon be replaced by `PANDAS_DataFrame.parquet`.",
                    DeprecationWarning,
                    stacklevel=2,
                )
                return deserialize_pandas_parquet(message)
            elif t == PANDAS_DF_PARQUET:
                return deserialize_pandas_parquet(message)
            elif t == DF or t == PDS:
                warnings.warn(
                    "`DataFrame` and `Series` is deprecated and will soon be replaced by `PANDAS_DataFrame` or `PANDAS_Series`.",
                    DeprecationWarning,
                    stacklevel=2,
                )
                return deserialize_pandas_json(message)
            elif t == PANDAS_DF or t == PANDAS_PDS:
                return deserialize_pandas_json(message)
            elif t == GDF or t == GPDS:
                return deserialize_geopandas_json(message)
            elif t == POLARS_DF:
                return deserialize_polars_json(message)
            elif t == NUMPY:
                return deserialize_numpy(message)

        # input is a "normal" dict
        return {k: message_to_python_types(v) for k, v in message.items()}

    # input is a list, tuple or set
    if isinstance(message, Collection) and not isinstance(message, str):
        return [message_to_python_types(k) for k in message]

    # return original input if it is anything else
    return message


def to_json(data: str) -> dict:
    return json.loads(data.replace("'", '"'))


def validify_url(url: str) -> str:
    """
    Remove leading part of URL
    """
    # Using 'ttps' because look-behind requires fixed-width pattern
    return re.sub(r"(?<!http:|ttps:)//", r"/", url)


def create_routing_table() -> Dict[str, Tuple[str, str]]:
    baseurl = "https://crux-nuclei.com"
    r = requests.get(baseurl + "/g/svc/api")
    if r.status_code != 200:  # pragma: no cover
        raise IOError("Could not connect to nuclei for routing tables")

    routes = dict()

    for app in r.json():
        # json schema example:
        # app: "gef-model"
        # url: "/api/gef-model/"
        # host_env: "GEF_MODEL_SERVICE_HOST"
        # port_env: "GEF_MODEL_SERVICE_PORT"

        app_name = app["app"]
        url = app["url"]
        host = os.environ.get(app["host_env"])
        port = os.environ.get(app["port_env"])
        routes[app_name] = (baseurl + url, f"http://{host}:{port}{url}")
    return routes


def token_time_valid(jwt: str) -> bool:
    """
    Check if the jwt is not expired.
    """
    payload = jwt.split(".")[1]
    # Here we decode the base64 encoded middle part of the JWT token. The length of the
    # payload needs to be a multi-fold of 4, so we pad it with "=" dummies if necessary.
    try:
        content: Dict = json.loads(
            base64.urlsafe_b64decode(
                payload + "=" * divmod(len(payload), 4)[1]
            ).decode()
        )
    except (binascii.Error, UnicodeDecodeError):
        return False

    # expiry time in seconds since unix epoch
    exp = content.get("exp")
    if exp is not None:
        return int(exp) > time.time()
    return True

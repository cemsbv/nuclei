import base64
import io
import json
import os
import warnings
from collections.abc import Collection, Mapping
from typing import Any, Union

try:
    import geopandas as gpd
    import numpy as np
    import pandas as pd
    import polars as pl
except ImportError:
    raise ImportError(
        "Could not import one of dependencies [geopandas, numpy, pandas, polars].  "
        "Must install nuclei[client] in order to use the utils functions"
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


def to_json(data: str) -> dict:
    return json.loads(data.replace("'", '"'))


def buffer_to_base64(buf: io.BytesIO) -> str:
    buf.seek(0)
    return base64.b64encode(buf.read()).decode("utf-8")


def base64_to_buffer(blob: bytes) -> io.BytesIO:
    blob = base64.b64decode(blob)
    buf = io.BytesIO()
    buf.write(blob)
    return buf


def deserialize_polars_json(message: dict) -> pl.DataFrame:
    """
    Only needed for backwards compatibility.
    """
    return pl.read_json(io.BytesIO(message["body"].encode("utf8")))


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
) -> Union[gpd.GeoDataFrame, gpd.GeoSeries, Any]:
    """
    Only needed for backwards compatibility.
    """
    obj = gpd.read_file(message["body"]).reset_index(drop=True)
    obj = obj.drop(columns="id")

    if len(obj.columns) == 1 and obj.columns[0] == "geometry":
        obj = obj.geometry

    return obj


def serialize_geopandas_json(obj: Union[gpd.GeoDataFrame, gpd.GeoSeries]) -> dict:
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
        gpd.GeoSeries,
        gpd.GeoDataFrame,
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
            if all(isinstance(x, (float, int)) for x in schema.flatten()):
                return json.loads(json.dumps(schema.tolist()).replace("NaN", "null"))
            else:
                return schema.tolist()
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
    gpd.GeoSeries,
    gpd.GeoDataFrame,
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
                    "`DataFrame` and `Series` is deprecated and will soon be replaced by `PANDAS_DataFrame` or "
                    "`PANDAS_Series`.",
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

from __future__ import annotations

import json
import warnings
from collections.abc import Collection, Mapping
from typing import Any

try:
    import numpy as np
    import orjson
except ImportError:
    raise ImportError(
        "Could not import one of dependencies [numpy, orjson]. "
        "Must install nuclei[client] in order to use the utils functions"
    )


def to_json(data: str) -> dict:
    return json.loads(data.replace("'", '"'))


def serialize_json_bytes(obj: Any) -> bytes:
    """
    Takes an object and converts it to a JSON-bytes-string. Uses orjson.dumps()
    to do the heavy lifting.

    Serializable objects are (amongst others):
        - python natives
        - dataclasses
        - datetime objects
        - numpy objects

    Some known objects that are not serializable:
        - numpy.float16
        - numpy.float128

    Options:
        - Serialize datetime.datetime objects without a tzinfo as UTC. This has no effect
          on datetime.datetime objects that have tzinfo set.
        - Serialize a UTC timezone on datetime.datetime instances as Z instead of +00:00
        - Serialize numpy.ndarray instances. For more, see numpy.

    Parameters
    ----------
    obj: Any
        The object to serialize

    Returns
    -------
    json-string: bytes
        a JSON bytes-string
    """
    return orjson.dumps(
        obj, option=orjson.OPT_SERIALIZE_NUMPY | orjson.OPT_NAIVE_UTC | orjson.OPT_UTC_Z
    )


def serialize_json_string(obj: Any) -> str:
    """
    Takes an object and converts it to a JSON-string. Uses orjson.dumps()
    to do the heavy lifting.

    Serializable objects are (amongst others):
        - python natives
        - dataclasses
        - datetime objects
        - numpy objects

    Some known objects that are not serializable:
        - numpy.float16
        - numpy.float128

    Parameters
    ----------
    obj: Any
        The object to serialize

    Returns
    -------
    json-string: str
        a JSON string
    """
    return serialize_json_bytes(obj).decode("utf-8")


def serialize_jsonifyable_object(
    obj: dict | np.ndarray | list | str | float | int | bool,
) -> Any:
    """
    Takes an object and converts it to a JSON-serializable object. Uses orjson.dumps()
    to do the heavy lifting.

    Serializable objects are (amongst others):
        - python natives
        - dataclasses
        - datetime objects
        - numpy objects

    Some known objects that are not serializable:
        - numpy.float16
        - numpy.float128


    Parameters
    ----------
    obj: Any
        The object to serialize

    Returns
    -------
    json-string: str
        a JSON string
    """
    return orjson.loads(serialize_json_bytes(obj))


def python_types_to_message(
    schema: dict | np.ndarray | list | str | float | int | bool,
) -> Any:
    """
    Cast python types to jsonifyable message.

    DEPRECATED since 0.5.0

    Parameters
    ----------
    schema

    Returns
    -------
    message
        jsonifyable message.
    """
    warnings.warn(
        "This function has been deprecated and will be removed in the future. It is "
        "recommended to use `nuclei.client.utils.serialize_jsonifyable_object` instead.",
        DeprecationWarning,
        stacklevel=2,
    )
    if isinstance(schema, np.ndarray):
        # no NaN in array
        if all(isinstance(x, (np.floating, np.integer)) for x in schema.flatten()):
            return json.loads(json.dumps(schema.tolist()).replace("NaN", "null"))
        else:
            return schema.tolist()
    if isinstance(schema, float) and np.isnan(schema):
        return None
    # recurse and convert to jsonifyable types
    if isinstance(schema, Mapping):
        return {k: python_types_to_message(v) for k, v in schema.items()}
    if isinstance(schema, Collection) and not isinstance(schema, str):
        return [python_types_to_message(k) for k in schema]
    return schema

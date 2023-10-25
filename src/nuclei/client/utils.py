import json
from collections.abc import Collection, Mapping
from typing import Any, Union

try:
    import numpy as np
except ImportError:
    raise ImportError(
        "Could not import one of dependencies [numpy]. "
        "Must install nuclei[client] in order to use the utils functions"
    )


def to_json(data: str) -> dict:
    return json.loads(data.replace("'", '"'))


def python_types_to_message(
    schema: Union[
        dict,
        np.ndarray,
        list,
        str,
        float,
        int,
        bool,
    ],
) -> Any:
    """
    Cast python types to jsonifyable message.

    Parameters
    ----------
    schema

    Returns
    -------
    message
        jsonifyable message.
    """
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

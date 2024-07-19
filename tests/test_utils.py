import numpy as np
import pytest

from nuclei.client.utils import serialize_jsonifyable_object


@pytest.mark.parametrize(
    "schema,expected",
    [
        (1, 1),
        (np.int8(1), int(1)),
        (np.int16(1), int(1)),
        (np.int32(1), int(1)),
        (np.int64(1), int(1)),
        (1.0, 1.0),
        (np.float32(1), float(1)),
        (np.float64(1), float(1)),
        ("str", "str"),
        (np.nan, None),
        (np.inf, None),
        ([1, 2, 3], [1, 2, 3]),
        ((1, 2, 3), [1, 2, 3]),
        ([1.0, 2.0, 3.0], [1.0, 2.0, 3.0]),
        ((1.0, 2.0, 3.0), [1.0, 2.0, 3.0]),
        (
            [1, np.int8(2), np.int16(3), np.int32(4), np.int64(5)],
            [1, 2, 3, 4, 5],
        ),
        (
            np.array([1, np.int8(2), np.int16(3), np.int32(4), np.int64(5)]),
            [1, 2, 3, 4, 5],
        ),
        (
            [1.0, np.float32(2), np.float64(3)],
            [1.0, 2.0, 3.0],
        ),
        (
            np.array([1.0, np.float32(2), np.float64(3)]),
            [1.0, 2.0, 3.0],
        ),
        (
            [True, np.bool_(True), False, np.bool_(False)],
            [True, True, False, False],
        ),
        (
            np.array([True, np.bool_(True), False, np.bool_(False)]),
            [True, True, False, False],
        ),
        (
            np.array([np.array([np.int16(1), 2.0]), np.array([np.nan, np.float32(4)])]),
            [[1.0, 2.0], [None, 4.0]],
        ),
        (
            {"str": "str", "list": np.array([np.nan, np.bool_(False), np.int32(3)])},
            {"str": "str", "list": [None, False, 3]},
        ),
    ],
)
def test_serialize(schema, expected):
    jsonifyable_object = serialize_jsonifyable_object(schema)
    assert jsonifyable_object == expected


def test_python_types_to_message_bool():
    # Test convert to jsonifyable object
    jsonifyable_object = serialize_jsonifyable_object(np.bool_(True))
    assert jsonifyable_object is True


def test_python_types_to_message_error():
    class Custom:
        def __init__(self):
            pass

    with pytest.raises(TypeError):
        serialize_jsonifyable_object(Custom())

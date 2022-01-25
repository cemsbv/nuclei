import json
import os

import numpy as np
import pandas as pd
import polars as pl
import pytest

from nuclei.utils import (
    deserialize_pandas_parquet,
    message_to_python_types,
    python_types_to_message,
    serialize_pandas_parquet,
    token_time_valid,
)

try:
    import geopandas as gpd
    from geopandas.testing import assert_geodataframe_equal, assert_geoseries_equal
except ImportError:
    gpd = None


def test_parquet_serialization():
    df = pd.DataFrame({"a": [1, 2]})
    blob = serialize_pandas_parquet(df)
    df_rcv = deserialize_pandas_parquet(blob)
    pd.testing.assert_frame_equal(df, df_rcv)

    series = pd.Series(data=[1, 2], index=[0, 1], name="a")
    blob = serialize_pandas_parquet(series)
    s_rcv = deserialize_pandas_parquet(blob)
    pd.testing.assert_frame_equal(df, s_rcv)


def convert_and_back(msg):
    msg = python_types_to_message(msg)

    # dict to json
    msg_json = json.dumps(msg)
    # json to dict
    msg = json.loads(msg_json)

    return message_to_python_types(msg)


def check_message_to_message(msg):
    pt = convert_and_back(msg)
    if gpd is not None:
        if isinstance(msg, gpd.GeoDataFrame):
            assert_geodataframe_equal(msg, pt, check_crs=False)
        elif isinstance(msg, gpd.GeoSeries):
            assert_geoseries_equal(msg, pt, check_crs=False)
    elif isinstance(msg, pd.DataFrame):
        pd.testing.assert_frame_equal(msg, pt)
    elif isinstance(msg, pd.Series):
        pd.testing.assert_series_equal(msg, pt)
    elif isinstance(msg, pl.DataFrame):
        msg.frame_equal(pt)


def test_gpd_message_to_message():
    """test the serialized and deserialize of a gpd.DataFrame/ Series"""
    if gpd is not None:
        check_message_to_message(
            gpd.GeoDataFrame({"a": [1, 2]}, geometry=gpd.points_from_xy([0, 1], [0, 1]))
        )
        check_message_to_message(gpd.GeoSeries(gpd.points_from_xy([0], [0])))


def test_polars_message_to_message():
    """test the serialized and deserialize of a polars.DataFrame"""
    check_message_to_message(pl.DataFrame({"a": [1, 2]}))


@pytest.mark.parametrize("force_serialization", ["", "1"])
def test_pandas_message_to_message(force_serialization):
    """test the serialized and deserialize of a pandas.DataFrame/ Series"""
    os.environ["FORCE_SERIALIZATION"] = force_serialization
    check_message_to_message(pd.Series({"a": [1, 2]}))
    check_message_to_message(pd.DataFrame({"a": [1, 2]}))


@pytest.mark.parametrize("force_serialization", ["", "1"])
def test_pandas_warn_message_to_message(force_serialization):
    """test the old deserialize of a pandas.DataFrame/ Series"""
    os.environ["FORCE_SERIALIZATION"] = force_serialization
    with pytest.warns(DeprecationWarning):
        message_to_python_types(
            {
                "body": pd.DataFrame({"a": [1, 2]}).to_json(),
                "nuclei": {"type": "DataFrame"},
            }
        )
    with pytest.warns(DeprecationWarning):
        message_to_python_types(
            {"body": pd.Series({"a": [1, 2]}).to_json(), "nuclei": {"type": "Series"}}
        )


@pytest.mark.parametrize("force_serialization", ["", "1"])
def test_dict_in_dataframe_fallback(force_serialization):
    os.environ["FORCE_SERIALIZATION"] = force_serialization
    check_message_to_message(pd.DataFrame({"a": [1, "test", {"x": 1, "y": 2}]}))


@pytest.mark.parametrize("force_serialization", ["", "1"])
def test_dict_to_dict(force_serialization):
    os.environ["FORCE_SERIALIZATION"] = force_serialization
    msg1 = {"df": pd.DataFrame({"a": [1, 2]})}
    msg2 = convert_and_back(msg1)
    assert msg1.keys() == msg2.keys() == {"df"}
    pd.testing.assert_frame_equal(msg1["df"], msg2["df"])


@pytest.mark.parametrize("force_serialization", ["", "1"])
def test_numpy(force_serialization):
    os.environ["FORCE_SERIALIZATION"] = force_serialization
    a = np.array([[1, 2], [2, 3]], dtype=np.float16)
    msg = {"param": a}
    resp = convert_and_back(msg)
    np.testing.assert_array_equal(a, resp["param"])


def test_numpy_all_types():
    os.environ["FORCE_SERIALIZATION"] = ""
    a = np.array([[np.int16(1), 2.0], [np.nan, np.float32(4)]])
    rsp = python_types_to_message(a)
    assert rsp == [[1.0, 2.0], [None, 4.0]]


@pytest.mark.parametrize("force_serialization", ["", "1"])
def test_list_str(force_serialization):
    os.environ["FORCE_SERIALIZATION"] = force_serialization
    msg = {"str": "str", "list": [1, 2, 3]}
    resp = convert_and_back(msg)
    assert msg == resp


def test_literals():
    s = "str"
    assert message_to_python_types(s) == s
    list_ = [1, 2, 3]
    assert message_to_python_types(list_) == list_


def test_time_expired():
    tkn = (
        "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9."
        "eyJpYXQiOjE2MTU4OTcxNjgsIm5iZiI6MTYxNT"
        "g5NzE2OCwianRpIjoiNmFjNWYzMWUtOTIwNS00Nj"
        "JiLTliNzgtMjY4NjIyM2UwOGMyIiwiZXhwIjoxNjE"
        "1OTQwMzY4LCJpZGVudGl0eSI6InJpdGNoaWU0NkBnb"
        "WFpbC5jb20iLCJmcmVzaCI6ZmFsc2UsInR5cGUiOiJ"
        "hY2Nlc3MiLCJ1c2VyX2NsYWltcyI6eyJhbGxvd2VkX2"
        "FjY2VzcyI6ImFkbWluIiwibGltaXQiOnsibnVsbCI6bnVsbH19fQ. "
        "M_Hyozg8KkWLz-mUpvpktbWCKwONp1pLwn9aufy3cPY"
    )

    assert not token_time_valid(tkn)

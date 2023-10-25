import numpy as np

from nuclei.client.utils import python_types_to_message


def test_numpy_all_types():
    a = np.array([[np.int16(1), 2.0], [np.nan, np.float32(4)]])
    rsp = python_types_to_message(a)
    assert rsp == [[1.0, 2.0], [None, 4.0]]

    a = np.array([[np.int16(1), 2.0, np.inf], [np.nan, np.float32(4), "abc"]])
    rsp = python_types_to_message(a)
    assert rsp == [["1", "2.0", "inf"], ["nan", "4.0", "abc"]]


def test_list_str():
    msg = {"str": "str", "list": [1, 2, 3]}
    resp = python_types_to_message(msg)
    assert msg == resp


def test_literals():
    s = "str"
    assert python_types_to_message(s) == s
    list_ = [1, 2, 3]
    assert python_types_to_message(list_) == list_

# pylint: disable=missing-function-docstring,missing-module-docstring

from typing import OrderedDict, Union

from pdxloc.util import read_localisation, write_localisation
from tests.named_temporary_file import named_temporary_file

_LANGUAGE_KEY = "l_english"


def test_read_data() -> None:
    valid_yaml = f"""{_LANGUAGE_KEY}:
 key1: hello
 key2: 42
"""
    with named_temporary_file() as temp_file:
        temp_file.write_text(valid_yaml, encoding="utf-8")
        data = read_localisation(temp_file)

    assert isinstance(data, OrderedDict), "Main data structure is not a OrderedDict"
    assert _LANGUAGE_KEY in data, "Language key is missing"
    assert data[_LANGUAGE_KEY], "Language value is empty or None"
    assert isinstance(
        data[_LANGUAGE_KEY], OrderedDict
    ), "Language value is not a OrderedDict"

    first_key = "key1"
    assert (
        first_key in data[_LANGUAGE_KEY]
    ), f"{first_key=} is not in {data[_LANGUAGE_KEY]=}"
    assert isinstance(
        data[_LANGUAGE_KEY][first_key], str
    ), f"Value of {first_key=} is not str"
    assert (
        data[_LANGUAGE_KEY][first_key] == "hello"
    ), f"Value of {first_key=} is not 'hello'"

    second_key = "key2"
    assert (
        second_key in data[_LANGUAGE_KEY]
    ), f"{second_key=} is not in {data[_LANGUAGE_KEY]=}"
    assert isinstance(
        data[_LANGUAGE_KEY][second_key], int
    ), f"Value of {second_key=} is not int"
    assert data[_LANGUAGE_KEY][second_key] == 42, f"Value of {second_key=} is not 42"


def test_write_data() -> None:
    data: OrderedDict[str, OrderedDict[str, Union[str, int]]] = OrderedDict(
        {
            _LANGUAGE_KEY: OrderedDict(
                {
                    "key1": "test",
                    "key2": 42,
                }
            )
        }
    )
    expected_output_with_byte_order_mark = f"""\ufeff{_LANGUAGE_KEY}:
 key1: "test"
 key2: "42"
"""
    with named_temporary_file() as temp_file:
        write_localisation(data, temp_file)
        assert expected_output_with_byte_order_mark == temp_file.read_text(
            encoding="utf-8"
        )


def test_read_write_round_trip() -> None:
    input_data = {
        _LANGUAGE_KEY: {
            "key": "test",
        }
    }
    with named_temporary_file() as temp_file:
        write_localisation(input_data, temp_file)
        output = read_localisation(temp_file)
    assert output == input_data, f"{input_data=} is not identical to {output=}"


def test_read_write_multi_line_strings() -> None:
    data = {
        _LANGUAGE_KEY: {
            "key": """first line\nsecond line\nthird line""",
        }
    }
    multi_line = r"first line\nsecond line\nthird line"
    expected_output_with_byte_order_mark = f"""\ufeff{_LANGUAGE_KEY}:
 key: "{multi_line}"
"""
    with named_temporary_file() as temp_file:
        write_localisation(data, temp_file)
        assert expected_output_with_byte_order_mark == temp_file.read_text(
            encoding="utf-8"
        ), "Multi-line strings should be span only one line"


def test_read_write_long_strings() -> None:
    very_long_string = "This is a sentence. " * 5000
    data = {
        _LANGUAGE_KEY: {
            "key": very_long_string,
        }
    }
    expected_output_with_byte_order_mark = f"""\ufeff{_LANGUAGE_KEY}:
 key: "{very_long_string}"
"""
    with named_temporary_file() as temp_file:
        write_localisation(data, temp_file)
        assert expected_output_with_byte_order_mark == temp_file.read_text(
            encoding="utf-8"
        ), "Long strings should not be broken up into multi-line entries"


def test_write_key_versioning() -> None:
    data = {
        _LANGUAGE_KEY: {
            "key1": "value1",
            "poland.13.b:0": "value2",
        }
    }
    expected_output_with_byte_order_mark = f"""\ufeff{_LANGUAGE_KEY}:
 key1: "value1"
 poland.13.b:0: "value2"
"""
    with named_temporary_file() as temp_file:
        write_localisation(data, temp_file)
        assert expected_output_with_byte_order_mark == temp_file.read_text(
            encoding="utf-8"
        ), "Key versioning should not fail"


def test_read_key_versioning() -> None:
    data = f"""\ufeff{_LANGUAGE_KEY}:
 key: "test"
 poland.13.b:0: "ok"
"""
    with named_temporary_file() as temp_file:
        temp_file.write_text(data, encoding="utf-8")
        output = read_localisation(temp_file)
        assert output == OrderedDict(
            {_LANGUAGE_KEY: OrderedDict({"key": "test", "poland.13.b:0": "ok"})}
        )

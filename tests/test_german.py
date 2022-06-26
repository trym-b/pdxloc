# pylint: disable=missing-function-docstring,missing-module-docstring

from pdxloc.util import read_localisation, write_localisation
from tests.named_temporary_file import named_temporary_file


def test_read_german_characters() -> None:
    language_key = "l_german"
    valid_yaml = """l_german:
 key: ßüöä
"""
    with named_temporary_file() as temp_file:
        temp_file.write_text(valid_yaml, encoding="utf-8")
        data = read_localisation(temp_file)

    key = "key"
    assert isinstance(data[language_key][key], str), f"Value of {key=} is not str"
    assert data[language_key][key] == "ßüöä", f"Value of {key} is not 'ßüöä'"


def test_write_german_characters() -> None:
    data = {
        "l_german": {
            "key": "ßüöä",
        }
    }
    expected_output_with_byte_order_mark = """l_german:
 key: "ßüöä"
"""
    with named_temporary_file() as temp_file:
        write_localisation(data, temp_file)
        result = temp_file.read_text(encoding="utf-8-sig")
        assert expected_output_with_byte_order_mark == result

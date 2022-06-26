# pylint: disable=missing-function-docstring,missing-module-docstring

from typing import OrderedDict

from pdxloc.util import read_localisation, write_localisation
from tests.named_temporary_file import named_temporary_file


def test_read_empty_file() -> None:
    with named_temporary_file() as temp_file:
        temp_file.write_text("", encoding="utf-8")
        data = read_localisation(temp_file)

    assert isinstance(data, OrderedDict), "Main data structure is not a OrderedDict"
    assert data == OrderedDict(), "Read data should be empty"


def test_write_empty_file() -> None:
    data: OrderedDict = OrderedDict()
    expected_output_with_byte_order_mark = """\ufeff"""
    with named_temporary_file() as temp_file:
        write_localisation(data, temp_file)
        assert expected_output_with_byte_order_mark == temp_file.read_text(
            encoding="utf-8"
        )

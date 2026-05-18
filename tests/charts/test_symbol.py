import pytest

from modules.charts.domain import Symbol


def test_symbol_to_string():
    symbol = Symbol.PURL
    string = symbol.to_string()
    assert string == "purl"

def test_symbol_from_string():
    string = "purl"
    symbol = Symbol.from_string(string)
    assert symbol == Symbol.PURL


def test_symbol_from_string_rejects_invalid_symbol():
    string = "invalid_symbol"

    with pytest.raises(Exception):
        Symbol.from_string(string)

def test_symbol_from_string_rejects_case_mismatch():
    string = "PURL"

    with pytest.raises(Exception):
        Symbol.from_string(string)

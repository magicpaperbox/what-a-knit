import pytest

from modules.charts.domain import Color


def test_color_to_string():
    color = Color("#ffffff")
    string = color.to_string()
    assert string == "#ffffff"

def test_color_from_string():
    string = "#ffffff"
    symbol = Color.from_string(string)
    assert symbol == Color("#ffffff")


def test_color_from_string_rejects_missing_hash():
    string = "ffffff"

    with pytest.raises(Exception):
        Color.from_string(string)

def test_color_from_string_rejects_incorrect_hex_values():
    string = "#g1g2h4"

    with pytest.raises(Exception):
        Color.from_string(string)

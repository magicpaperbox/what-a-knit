import pytest
from pytest import fail
from modules.charts.domain import SymbolChart, Symbol


def test_rectangular_chart():
    chart = SymbolChart(
        id=None,
        name="Test",
        cell_size=10,
        cells=[
            [None, Symbol.PURL, Symbol.PURL],
            [Symbol.SSK, Symbol.PURL, None]
        ])
    chart.validate()

def test_not_rectangular_chart():
    chart = SymbolChart(
        id=None,
        name="Test",
        cell_size=10,
        cells=[
            [None, Symbol.PURL, Symbol.PURL],
            [Symbol.SSK, Symbol.PURL]
        ])
    try:
        chart.validate()
        fail("Expected validation failure")
    except ValueError as error:
        assert str(error) == "Length of the row is not correct"
    except Exception as error:
        fail(f"Unexpected exception {error}")


def test_empty_row():
    chart = SymbolChart(
        id=None,
        name="Test",
        cell_size=10,
        cells=[
            [],
            []
        ])
    try:
        chart.validate()
        fail("Expected validation failure")
    except ValueError as error:
        assert str(error) == "Empty row!"
    except Exception as error:
        fail(f"Unexpected exception {error}")

def test_empty_chart():
    chart = SymbolChart(
        id=None,
        name="Test",
        cell_size=10,
        cells=[]
    )

    with pytest.raises(ValueError, match="Chart has no cells!"):
        chart.validate()

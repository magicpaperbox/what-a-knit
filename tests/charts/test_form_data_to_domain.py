
from modules.charts.domain import SymbolChart, Symbol
from modules.charts.mappers import ChartFormData


def test_form_data_to_domain():
    form_data = ChartFormData(
        name="Test",
        rows="2",
        columns="3",
        cell_size="10",
        cells_json='[[null, "purl", "purl"],["ssk", "purl", null]]',
        kind="symbol"
    )
    chart = form_data.to_domain()
    assert SymbolChart(
        id=None,
        name="Test",
        cell_size=10,
        cells=[
            [None, Symbol.PURL, Symbol.PURL],
            [Symbol.SSK, Symbol.PURL, None]
        ]
    ) == chart
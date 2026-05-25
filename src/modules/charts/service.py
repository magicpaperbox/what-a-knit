from modules.charts.domain import Chart
from modules.charts.repository import ChartRepository


class ChartService:
    def __init__(self):
        self._chart_repository = ChartRepository()

    def add_chart(self, chart: Chart) -> Chart:
        chart.validate()
        return self._chart_repository.add(chart)

    def update_chart(self, chart: Chart) -> Chart:
        chart.validate()
        return self._chart_repository.update(chart)
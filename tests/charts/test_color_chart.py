from modules.charts.domain import ColorChart, Color


def test_all_colors():
    blue = Color.from_string('#277DF5')
    red = Color.from_string('#F54927')
    test_chart = ColorChart(
        id=None,
        name="new",
        cell_size=5,
        cells=[
            [red, blue],
            [blue, None]
        ]
    )
    colors = test_chart.all_colors()
    assert colors == [blue, red]

   # [_, _, _, _, _]

# @dataclass
# class Food:
#     name: str
#     price: int
#
#     def __hash__(self) -> int:
#         return hash(self.name) + self.price
#
#     def __eq__(self, other):
#         return other.price == self.price and self.name == other.name
#
# potato = Food(name="potato", price=1)
#
# hash(potato) == 4354325345
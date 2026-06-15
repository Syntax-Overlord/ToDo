from textual.app import App, ComposeResult
from textual.widgets import DataTable


class TableApp(App):
    def compose(self) -> ComposeResult:
        yield DataTable()

    def on_mount(self) -> None:
        table = self.query_one(DataTable)

        data = [
            ["ID", "Name", "Score"],  # header row
            [1, "Alice", 90],
            [2, "Bob", 85],
            [3, "Charlie", 92],
        ]

        # first row = columns (header)
        headers = data[0]
        table.add_columns(*headers)

        # rest = rows
        for row in data[1:]:
            table.add_row(*row)


if __name__ == "__main__":
    TableApp().run()

from textual.app import App, ComposeResult
from textual.app import ComposeResult
from textual.containers import VerticalScroll, HorizontalGroup
from textual.widgets import Static, Input, Button, DataTable
from rich.text import Text
from ascii_art import (
    login,
    sign_in,
    add_task,
    add_task_heading,
    complete_task,
    complete_task_heading,
    remove_task,
    remove_task_heading,
)
from database import Database
import re
from datetime import datetime, timedelta


class Login(VerticalScroll):

    def compose(self) -> ComposeResult:
        yield Static(login, classes="login_heading")
        yield Input(placeholder="Username", id="username")
        yield Input(placeholder="Password", id="password")
        yield Button(sign_in, id="sign_in")


class Add_Task(VerticalScroll):

    def compose(self) -> ComposeResult:
        yield Static(add_task_heading, classes="add_tasks_heading")
        yield Input(placeholder="Title", id="task_title")
        yield Input(placeholder="Description", id="task_description")
        yield Input(placeholder="Due Date (DD-MM-YYYY)", id="task_due_date")
        yield Button(add_task, id="add_task")

    def on_input_changed(self, event: Input.Changed) -> None:
        """Validate date format on the due_date input."""
        if event.input.id == "task_due_date":
            value = event.value
            if value and not re.match(r"^\d{2}-\d{2}-\d{4}$", value):
                # Invalid format, clear the input
                event.input.value = ""


class Complete_Task(VerticalScroll):

    def compose(self) -> ComposeResult:
        yield Static(complete_task_heading, classes="add_tasks_heading")
        yield Input(placeholder="Task ID", id="task_id")
        yield Button(complete_task, id="complete_task")


class Remove_Task(VerticalScroll):

    def compose(self) -> ComposeResult:
        yield Static(remove_task_heading, classes="add_tasks_heading")
        yield Input(placeholder="Task ID", id="task_id")
        yield Button(remove_task, id="remove_task")


class View_Tasks(VerticalScroll):

    def __init__(self, table_name: str):
        super().__init__()
        self.database_connection = Database(table_name=table_name)
        self._table_columns = []

    def compose(self) -> ComposeResult:
        yield DataTable(show_row_labels=False)

    def _stretch_table_columns(self) -> None:
        table = self.query_one(DataTable)

        if not self._table_columns:
            return

        available_width = max(table.size.width - 2, 1)
        weights = [2, 7, 8, 6, 5]
        total_weight = sum(weights)

        widths = [
            max(8, (available_width * weight) // total_weight) for weight in weights
        ]
        extra_width = available_width - sum(widths)
        if widths:
            widths[-1] += extra_width

        for column_key, width in zip(self._table_columns, widths):
            column = table.columns[column_key]
            column.width = max(width, 1)
            column.auto_width = False

        table.refresh()

    def on_mount(self) -> None:
        table = self.query_one(DataTable)

        header = [
            Text("I D", justify="center"),
            Text("T A S K  T I T L E", justify="center"),
            Text("D E S C R I P T I O N", justify="center"),
            Text("D U E  D A T E", justify="center"),
            Text("S T A T U S", justify="center"),
        ]

        self._table_columns = table.add_columns(*header)

        rows = self.database_connection.get_tasks()

        today = datetime.now().date()

        for row in rows:
            task_id, task_title, description, due_date_str, status = row

            # Check if task is overdue and mark as completed if necessary
            if status == "pending" and due_date_str:
                try:
                    due_date = datetime.strptime(due_date_str, "%d-%m-%Y").date()
                    if due_date < today:
                        self.database_connection.complete_task(task_id)
                        status = "completed"
                except ValueError:
                    pass

            # Create colored due date text
            due_date_text = Text(due_date_str if due_date_str else "", justify="center")
            if due_date_str and status != "completed":
                try:
                    due_date = datetime.strptime(due_date_str, "%d-%m-%Y").date()
                    days_until = (due_date - today).days

                    if days_until >= 7:
                        color = "green"
                    elif days_until >= 1:
                        color = "yellow"
                    else:
                        color = "red"

                    due_date_text = Text(
                        due_date_str, justify="center", style=f"{color}"
                    )
                except ValueError:
                    pass
            elif status == "completed":
                due_date_text = Text(
                    due_date_str if due_date_str else "",
                    justify="center",
                    style="white",
                )

            # Center all cell content
            centered_row = [
                Text(str(task_id), justify="center"),
                Text(str(task_title), justify="center"),
                Text(str(description), justify="center"),
                due_date_text,
                Text(str(status), justify="center"),
            ]

            table.add_row(*centered_row)

        self._stretch_table_columns()

    def on_resize(self) -> None:
        self._stretch_table_columns()

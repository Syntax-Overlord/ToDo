from textual.app import App, ComposeResult
from textual.app import ComposeResult
from textual.containers import VerticalScroll
from textual.widgets import Static, Input, Button
from ascii_art import login, sign_in, add_task, add_task_heading


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

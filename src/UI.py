from textual.app import App, ComposeResult
from textual.containers import HorizontalGroup, VerticalScroll, Container
from textual.widgets import Header, Footer, Static, Input, Button
from ascii_art import logo, login, sign_in


class Login(VerticalScroll):

    def compose(self):
        yield Static(login, classes="login_heading")
        yield Input(placeholder="Username", id="username")
        yield Input(placeholder="Password", id="password")
        yield Button(sign_in, id="sign_in")


class UI(App):

    CSS_PATH = "../styles/styles.tcss"
    BINDINGS = [
        ("A", "add_task", "Add Task"),
        ("C", "complete_task", "Complete Task"),
        ("R", "remove_task", "Remove Task"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        yield Static(logo, classes="logo")
        yield Container(HorizontalGroup(Login(), id="main"), id="outer_shell")


app = UI()
app.run()

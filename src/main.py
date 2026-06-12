from textual.app import App, ComposeResult
from textual.containers import HorizontalGroup, Container
from textual.widgets import Header, Footer, Static
from ascii_art import logo
from widgets import Login


class UI(App):

    CSS_PATH = "../styles/styles.tcss"
    BINDINGS = [
        ("A", "add_task", "Add Task"),
        ("C", "complete_task", "Complete Task"),
        ("R", "remove_task", "Remove Task"),
    ]

    def __init__(self):
        super().__init__()
        self.login = False
        self.username = None
        self.table = None

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        yield Static(logo, classes="logo")
        yield Container(HorizontalGroup(Login(), id="main"), id="outer_shell")


if __name__ == "__main__":
    app = UI()
    app.run()

# from textual.app import App, ComposeResult
from textual.containers import VerticalScroll
from textual.widgets import Static, Input, Button
from ascii_art import login, sign_in


class Login(VerticalScroll):

    def compose(self):
        yield Static(login, classes="login_heading")
        yield Input(placeholder="Username", id="username")
        yield Input(placeholder="Password", id="password")
        yield Button(sign_in, id="sign_in")

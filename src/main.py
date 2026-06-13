from textual.app import App, ComposeResult
from textual.containers import HorizontalGroup, Container
from textual.widgets import Header, Footer, Static, Button, Input
from ascii_art import logo
from widgets import Login, Add_Task
from credentials import Credential


class ToDo(App):

    CSS_PATH = "../styles/styles.tcss"
    BINDINGS = [
        ("L", "login_logout", "Login/Logout"),
        ("A", "add_task", "Add Task"),
        ("C", "complete_task", "Complete Task"),
        ("R", "remove_task", "Remove Task"),
    ]

    def __init__(self):
        super().__init__()
        self.login = False
        self.username = None
        self.table = None
        self.cred = Credential()

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        button_id = event.button.id

        if button_id == "sign_in":
            username = self.query_one("#username", Input).value
            password_ = self.query_one("#password", Input).value
            credentials_matched = self.cred.verify_user_id(
                username=username, password=password_
            )
            if credentials_matched:
                self.username = username
                self.table = self.cred.return_table_name(username)
                self.login = True

                await self.action_add_task()

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        yield Static(logo, classes="logo")
        yield Container(HorizontalGroup(Login(), id="main"), id="outer_shell")

    async def action_add_task(self) -> None:
        if self.login:
            main = self.query_one("#main")

            # If an Add_Task is already present, do nothing
            try:
                main.query_one(Add_Task)
                return
            except Exception:
                pass

            # Remove all existing children
            for child in list(main.children):
                await child.remove()

            # Add the Add_Task widget
            await main.mount(Add_Task())

    async def action_login_logout(self) -> None:
        main = self.query_one("#main")

        # Logout
        if self.login:
            self.login = False
            self.username = None

            for child in list(main.children):
                await child.remove()

            await main.mount(Login())
            return

        # Already on login screen
        try:
            main.query_one(Login)
            return
        except Exception:
            pass

        # Not logged in and login screen not visible
        for child in list(main.children):
            await child.remove()

        await main.mount(Login())


if __name__ == "__main__":
    app = ToDo()
    app.run()

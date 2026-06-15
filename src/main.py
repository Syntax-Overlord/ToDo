from textual.app import App, ComposeResult
from textual.containers import HorizontalGroup, Container
from textual.widgets import Header, Footer, Static, Button, Input
from ascii_art import logo
from widgets import Login, Add_Task, View_Tasks, Complete_Task, Remove_Task
from credentials import Credential


class ToDo(App):

    CSS_PATH = "../styles/styles.tcss"
    BINDINGS = [
        ("l", "login_logout", "Login/Logout"),
        ("v", "view_tasks", "Home Page"),
        ("a", "add_task", "Add Task"),
        ("c", "complete_task", "Complete Task"),
        ("r", "remove_task", "Remove Task"),
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

                await self.action_view_tasks()

        elif button_id == "add_task":
            task_title = self.query_one("#task_title", Input).value
            task_description = self.query_one("#task_description", Input).value
            task_due_date = self.query_one("#task_due_date", Input).value

            if self.login and self.table:
                from database import Database

                db = Database(table_name=self.table)
                db.add_task(task_title, task_description, task_due_date)
                db.close()

                # Clear the inputs
                self.query_one("#task_title", Input).value = ""
                self.query_one("#task_description", Input).value = ""
                self.query_one("#task_due_date", Input).value = ""

                # Refresh the view
                await self.action_view_tasks()

        elif button_id == "complete_task":
            task_id_str = self.query_one("#task_id", Input).value
            if self.login and self.table and task_id_str:
                try:
                    task_id = int(task_id_str)
                    from database import Database

                    db = Database(table_name=self.table)
                    db.complete_task(task_id)
                    db.close()

                    self.query_one("#task_id", Input).value = ""
                    await self.action_view_tasks()
                except ValueError:
                    pass

        elif button_id == "remove_task":
            task_id_str = self.query_one("#task_id", Input).value
            if self.login and self.table and task_id_str:
                try:
                    task_id = int(task_id_str)
                    from database import Database

                    db = Database(table_name=self.table)
                    db.delete_task(task_id)
                    db.close()

                    self.query_one("#task_id", Input).value = ""
                    await self.action_view_tasks()
                except ValueError:
                    pass

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        yield Static(logo, classes="logo")
        yield Container(HorizontalGroup(Login(), id="main"), id="outer_shell")

    async def action_view_tasks(self) -> None:
        if self.login:
            main = self.query_one("#main")

            try:
                main.query_one(View_Tasks)
                return
            except Exception:
                pass

            for child in list(main.children):
                await child.remove()

            await main.mount(View_Tasks(self.table or ""))

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

    async def action_complete_task(self) -> None:
        if self.login:
            main = self.query_one("#main")

            try:
                main.query_one(Complete_Task)
                return
            except Exception:
                pass

            for child in list(main.children):
                await child.remove()

            await main.mount(Complete_Task())

    async def action_remove_task(self) -> None:
        if self.login:
            main = self.query_one("#main")

            try:
                main.query_one(Remove_Task)
                return
            except Exception:
                pass

            for child in list(main.children):
                await child.remove()

            await main.mount(Remove_Task())

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

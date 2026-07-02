import sqlite3
from pathlib import Path


class Credential:

    def __init__(self) -> None:
        """
        Connects with credentials.db and creates cursor object.
        """

        database_path = (
            Path(__file__).resolve().parent.parent / "data" / "credentials.db"
        )
        database_path.parent.mkdir(parents=True, exist_ok=True)

        self.conn = sqlite3.connect(database_path)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        self.table_name: str = self.table()

    def _make_table_name(self, username: str, password: str) -> str:
        return f"{username}_{password}"

    def verify_user_id(self, username: str, password: str) -> bool:
        """
        Accepts username and password as arguments.

        Returns True if credentials are correct or if account doesn't exist (creates account).
        Returns False if credentials are incorrect.
        """

        username = username.lower().strip()
        table_name = self._make_table_name(username, password)

        # 1. Check if user exists
        self.cursor.execute(
            f"""
            SELECT password_hash, table_name
            FROM {self.table_name}
            WHERE username = ?
            """,
            (username,),
        )

        row = self.cursor.fetchone()

        # 2. If user does NOT exist → create user
        if row is None:
            self.cursor.execute(
                f"""
                INSERT INTO {self.table_name} (username, password_hash, table_name)
                VALUES (?, ?, ?)
                """,
                (username, password, table_name),
            )
            self.conn.commit()
            return True

        # 3. If user exists → verify password
        stored_password = row["password_hash"]

        if stored_password == password:
            if not row["table_name"]:
                self.cursor.execute(
                    f"""
                    UPDATE {self.table_name}
                    SET table_name = ?
                    WHERE username = ?
                    """,
                    (table_name, username),
                )
                self.conn.commit()
            return True

        return False

    def table(self) -> str:
        """
        Connects with table (creates it if it doesn't exist).
        """

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            password_hash TEXT,
            table_name TEXT
            );""")
        self.cursor.execute("PRAGMA table_info(users)")
        columns = {row["name"] for row in self.cursor.fetchall()}

        if "table_name" not in columns:
            self.cursor.execute("ALTER TABLE users ADD COLUMN table_name TEXT")

        self.conn.commit()
        return "users"

    def return_table_name(self, username: str) -> str:
        username = username.lower().strip()
        self.cursor.execute(
            f"""SELECT table_name FROM {self.table_name}
                            WHERE username = ?
                            """,
            (username,),
        )
        row = self.cursor.fetchone()

        if row is None or not row["table_name"]:
            return username

        return str(row["table_name"])

    def close(self) -> None:
        """
        Closes the sql connection.
        """
        self.conn.close()

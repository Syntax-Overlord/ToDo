import sqlite3


class Credential:

    def __init__(self):
        """
        Connects with credentials.db and creates cursor object.
        """

        self.conn = sqlite3.connect("../data/credentials.db")
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        self.table_name = self.table()

    def verify_user_id(self, username: str, password: str) -> bool:
        """
        Accepts username and password as arguments.

        Returns True if credentials are correct or if account doesn't exist (creates account).
        Returns False if credentials are incorrect.
        """

        username = username.lower().strip()

        # 1. Check if user exists
        self.cursor.execute(
            f"""
            SELECT password_hash
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
                INSERT INTO {self.table_name} (username, password_hash)
                VALUES (?, ?)
                """,
                (username, password),
            )
            self.conn.commit()
            return True

        # 3. If user exists → verify password
        stored_password = row["password_hash"]

        if stored_password == password:
            return True

        return False

    def table(self) -> str:
        """
        Connects with table (creates it if it doesn't exist).
        """

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            password_hash TEXT
            );""")
        self.conn.commit()
        return "users"

    def close(self) -> None:
        """
        Closes the sql connection.
        """
        self.conn.close()

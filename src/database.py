import sqlite3


class Database:

    def __init__(self, db_name: str):
        self.active_table = None

        self.conn = sqlite3.connect(db_name)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()

    def _require_table(self):
        if not self.active_table:
            raise ValueError("No active table selected")

    def _table(self):
        self._require_table()
        return self.active_table

    def _initialize_table(self):
        self._require_table()
        self.cursor.execute(f"""CREATE TABLE IF NOT EXISTS {self.active_table} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    task TEXT NOT NULL,
                    description TEXT,
                    due_date TEXT,
                    status TEXT DEFAULT 'pending',
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                    );""")
        self.conn.commit()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def login(self, table_name: str):
        self.active_table = table_name

        self._initialize_table()

    def logout(self):
        self.active_table = None

    def close(self):
        self.conn.close()

    def get_tasks(self):
        table_name = self._table()

        return self.cursor.execute(f"""SELECT * FROM {table_name};""").fetchall()

    def add_task(
        self,
        task: str,
        description: str,
        due_date: str,
    ):
        table_name = self._table()

        self.cursor.execute(
            f"""
                INSERT INTO {table_name}
                (task, description, due_date)
                VALUES (?, ?, ?)
                """,
            (task, description, due_date),
        )
        self.conn.commit()

    def complete_task(self, task_id: int):
        table_name = self._table()
        self.cursor.execute(
            f"UPDATE {table_name} SET status = ? WHERE id = ?", ("completed", task_id)
        )
        self.conn.commit()

    def delete_task(self, task_id: int):
        table_name = self._table()
        self.cursor.execute(f"DELETE FROM {table_name} WHERE id = ?", (task_id,))
        self.conn.commit()

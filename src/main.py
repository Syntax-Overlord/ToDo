import mysql.connector
import pickle
import os
import csv
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich import box
console = Console()
CONFIG_FILE = "db_config.dat"
def display_logo():
    """Display colorful ASCII logo for ToDo CLI."""
    logo = """████████╗ ██████╗ ██████╗  ██████╗     ██╗     ██╗███████╗████████╗
╚══██╔══╝██╔═══██╗██╔══██╗██╔═══██╗    ██║     ██║██╔════╝╚══██╔══╝
   ██║   ██║   ██║██║  ██║██║   ██║    ██║     ██║███████╗   ██║   
   ██║   ██║   ██║██║  ██║██║   ██║    ██║     ██║╚════██║   ██║   
   ██║   ╚██████╔╝██████╔╝╚██████╔╝    ███████╗██║███████║   ██║   
   ╚═╝    ╚═════╝ ╚═════╝  ╚═════╝     ╚══════╝╚═╝╚══════╝   ╚═╝   """
    # Create gradient effect with rich colors
    lines = logo.strip().split("\n")
    colors = ["bright_magenta", "magenta", "blue", "cyan", "bright_cyan", "bright_blue"]
    for i, line in enumerate(lines):
        text = Text(line, style=colors[i % len(colors)])
        console.print(text, justify="center")
    # Add tagline
    tagline = Text("✨ Organize Your Life, One Task at a Time ✨", style="bold yellow")
    console.print(tagline, justify="center")
    console.print()
def save_config(config):
    """Save MySQL configuration to file using pickle."""
    with open(CONFIG_FILE, "wb") as f:
        pickle.dump(config, f)
def load_config():
    """Load MySQL configuration from file."""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "rb") as f:
            return pickle.load(f)
    return None
def get_mysql_details():
    """Get MySQL connection details from user."""
    console.print("\n[bold cyan]MySQL Configuration[/bold cyan]")
    host = input("Enter MySQL Host (default: localhost): ") or "localhost"
    user = input("Enter MySQL User (default: root): ") or "root"
    password = input("Enter MySQL Password: ")
    database = input("Enter Database Name: ")
    config = [host, user, password, database]
    save_config(config)
    return config
def connect_db(config):
    """Connect to MySQL database."""
    try:
        conn = mysql.connector.connect(
            host=config[0], user=config[1], password=config[2]
        )
        cursor = conn.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS {}".format(config[3]))
        cursor.close()
        conn.close()
        conn = mysql.connector.connect(
            host=config[0], user=config[1], password=config[2], database=config[3]
        )
        return conn
    except mysql.connector.Error as e:
        console.print("[bold red]Error connecting to MySQL: {}[/bold red]".format(e))
        return None
def create_table(conn):
    """Create tasks table if not exists."""
    cursor = conn.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS tasks (
            id INT AUTO_INCREMENT PRIMARY KEY,
            task VARCHAR(255) NOT NULL,
            description TEXT,
            due_date DATETIME,
            status VARCHAR(20) DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)"""
    )
    conn.commit()
    cursor.close()
def add_task(conn):
    """Add a new task to database."""
    console.print("\n[bold green]Add New Task[/bold green]")
    task = input("Task Title: ")
    description = input("Description: ")
    due_date_str = input("Due Date (YYYY-MM-DD HH:MM): ")
    try:
        due_date = datetime.strptime(due_date_str, "%Y-%m-%d %H:%M")
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO tasks (task, description, due_date) VALUES (%s, %s, %s)",
            (task, description, due_date),
        )
        conn.commit()
        cursor.close()
        console.print("[bold green]Task added successfully![/bold green]")
    except ValueError:
        console.print("[bold red]Invalid date format![/bold red]")
    except mysql.connector.Error as e:
        console.print("[bold red]Error: {}[/bold red]".format(e))
def view_tasks(conn):
    """View all tasks with urgency highlighting."""
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, task, description, due_date, status FROM tasks ORDER BY due_date"
    )
    tasks = cursor.fetchall()
    cursor.close()
    if not tasks:
        console.print("[yellow]No tasks found![/yellow]")
        return
    table = Table(title="📋 Your Tasks", box=box.ROUNDED)
    table.add_column("ID", style="cyan", justify="center")
    table.add_column("Task", style="magenta")
    table.add_column("Description", style="white")
    table.add_column("Due Date", style="yellow")
    table.add_column("Status", justify="center")
    now = datetime.now()
    for task_id, task, desc, due_date, status in tasks:
        if due_date:
            time_diff = due_date - now
            hours_left = time_diff.total_seconds() / 3600
            if hours_left < 0:
                urgency = "[bold red]OVERDUE![/bold red]"
                task_style = "[bold red]"
            elif hours_left < 24:
                urgency = "[red]Urgent![/red]"
                task_style = "[red]"
            elif hours_left < 72:
                urgency = "[yellow]Soon[/yellow]"
                task_style = "[yellow]"
            else:
                urgency = "[green]On Time[/green]"
                task_style = "[green]"
            due_str = "{} {}".format(due_date.strftime("%Y-%m-%d %H:%M"), urgency)
        else:
            due_str = "No deadline"
            task_style = ""
        status_color = "[green]" if status == "completed" else "[yellow]"
        table.add_row(
            str(task_id),
            "{}{}[/]".format(task_style, task),
            desc or "",
            due_str,
            "{}{}[/]".format(status_color, status),
        )
    console.print(table)
def update_task(conn):
    """Update task status."""
    view_tasks(conn)
    task_id = input("\nEnter Task ID to mark as completed: ")
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET status = 'completed' WHERE id = %s", (task_id,))
    conn.commit()
    cursor.close()
    if cursor.rowcount > 0:
        console.print("[bold green]Task marked as completed![/bold green]")
    else:
        console.print("[bold red]Task not found![/bold red]")
def delete_task(conn):
    """Delete a task."""
    view_tasks(conn)
    task_id = input("\nEnter Task ID to delete: ")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
    conn.commit()
    cursor.close()
    if cursor.rowcount > 0:
        console.print("[bold green]Task deleted successfully![/bold green]")
    else:
        console.print("[bold red]Task not found![/bold red]")
def export_to_csv(conn):
    """Export all tasks to CSV file."""
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, task, description, due_date, status, created_at FROM tasks"
    )
    tasks = cursor.fetchall()
    cursor.close()
    filename = "tasks_export_{}.csv".format(datetime.now().strftime("%Y%m%d_%H%M%S"))
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(
            ["ID", "Task", "Description", "Due Date", "Status", "Created At"]
        )
        writer.writerows(tasks)
    console.print("[bold green]Data exported to {}![/bold green]".format(filename))
def import_from_csv(conn):
    """Import tasks from CSV file."""
    filename = input("Enter CSV filename: ")
    if not os.path.exists(filename):
        console.print("[bold red]File not found![/bold red]")
        return
    try:
        with open(filename, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader)
            cursor = conn.cursor()
            for row in reader:
                if len(row) >= 5:
                    cursor.execute(
                        "INSERT INTO tasks (task, description, due_date, status) VALUES (%s, %s, %s, %s)",
                        (row[1], row[2], row[3] if row[3] else None, row[4]),
                    )
            conn.commit()
            cursor.close()
        console.print("[bold green]Data imported successfully![/bold green]")
    except Exception as e:
        console.print("[bold red]Error importing data: {}[/bold red]".format(e))
def change_mysql_details():
    """Change MySQL connection details."""
    if os.path.exists(CONFIG_FILE):
        os.remove(CONFIG_FILE)
    console.print("[yellow]Configuration deleted. Please enter new details.[/yellow]")
    return get_mysql_details()
def display_menu():
    """Display main menu."""
    menu = Panel(
        "[bold cyan]1.[/] Add Task\n"
        "[bold cyan]2.[/] View Tasks\n"
        "[bold cyan]3.[/] Mark Task Complete\n"
        "[bold cyan]4.[/] Delete Task\n"
        "[bold cyan]5.[/] Export to CSV\n"
        "[bold cyan]6.[/] Import from CSV\n"
        "[bold cyan]7.[/] Change MySQL Details\n"
        "[bold cyan]8.[/] Exit",
        title="[bold magenta]📝 Main Menu[/bold magenta]",
        border_style="bright_blue",
        box=box.DOUBLE,
    )
    console.print(menu)
def main():
    """Main function to run the ToDo CLI application."""
    display_logo()
    config = load_config()
    if not config:
        console.print("[yellow]First time setup - Please enter MySQL details[/yellow]")
        config = get_mysql_details()
    conn = connect_db(config)
    if not conn:
        console.print("[bold red]Failed to connect to database. Exiting...[/bold red]")
        return
    create_table(conn)
    while True:
        display_menu()
        choice = input("\nEnter your choice: ")
        if choice == "1":
            add_task(conn)
        elif choice == "2":
            view_tasks(conn)
        elif choice == "3":
            update_task(conn)
        elif choice == "4":
            delete_task(conn)
        elif choice == "5":
            export_to_csv(conn)
        elif choice == "6":
            import_from_csv(conn)
        elif choice == "7":
            conn.close()
            config = change_mysql_details()
            conn = connect_db(config)
            if not conn:
                console.print("[bold red]Failed to connect. Exiting...[/bold red]")
                break
            create_table(conn)
        elif choice == "8":
            console.print(
                "[bold green]Thanks for using ToDo CLI! Goodbye! 👋[/bold green]"
            )
            conn.close()
            break
        else:
            console.print("[bold red]Invalid choice! Please try again.[/bold red]")
        input("\nPress Enter to continue...")
        console.clear()
        display_logo()
main()

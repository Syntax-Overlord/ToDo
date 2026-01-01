# 📋 ToDo List Application - MySQL Edition

## Project Overview

A professional CLI-based ToDo List Application built with Python that uses MySQL for data persistence, features colored terminal output using the Rich library, and provides CSV import/export functionality.

---

## ✨ Key Features

- **MySQL Database**: Stores all tasks in MySQL database with automatic table creation
- **Colored Terminal Output**: Rich library for beautiful styled text and tables
- **First-Time Setup**: Automatic MySQL configuration on first run
- **Configuration Management**: MySQL credentials stored securely using pickle
- **CSV Import/Export**: Transfer data between systems
- **Task Management**: Full CRUD operations (Create, Read, Update, Delete)
- **Urgency Highlighting**: Color-coded tasks based on due date proximity
- **Status Tracking**: Mark tasks as completed or pending

---

## 🎯 Completed Features

- [x] MySQL database integration with mysql.connector
- [x] First-time configuration wizard
- [x] Configuration persistence using pickle (.dat file)
- [x] Automatic database and table creation
- [x] Add Task with due date and description
- [x] View Tasks with urgency color coding:
  - Red: Overdue tasks
  - Red: Urgent (< 24 hours)
  - Yellow: Soon (< 72 hours)
  - Green: On time
- [x] Mark Task as Complete
- [x] Delete Task
- [x] Export data to CSV with timestamp
- [x] Import data from CSV
- [x] Change MySQL details option
- [x] Rich-styled menu and ASCII logo
- [x] Datetime-based urgency checking

---

## 📦 Required Libraries

Install using pip:

```bash
pip install mysql-connector-python rich
```

### Dependencies:

- `mysql-connector-python` - MySQL database connectivity
- `rich` - Terminal styling and colors
- `pickle` - Configuration storage (built-in)
- `csv` - Data export/import (built-in)
- `datetime` - Date/time handling (built-in)
- `os` - File operations (built-in)

---

## 📁 File Structure

```
ToDo/src/
├── main.py           # Main application with all functions
├── logo.py           # Rich-styled ASCII logo
├── test.py           # Testing file
├── ToDo.md           # This documentation
└── db_config.dat     # MySQL config (created on first run)
```

---

## 🛠️ Technical Details

### Database Schema

**Table: tasks**
| Column | Type | Description |
| ----------- | ------------ | ------------------------------ |
| id | INT (PK) | Auto-incrementing task ID |
| task | VARCHAR(255) | Task title |
| description | TEXT | Task description |
| due_date | DATETIME | Due date and time |
| status | VARCHAR(20) | pending/completed |
| created_at | TIMESTAMP | Creation timestamp |

### How to Run

1. Ensure MySQL server is running
2. Install dependencies: `pip install mysql-connector-python rich`
3. Run: `python main.py`
4. On first run, enter MySQL credentials
5. Database and table are created automatically

---

## 🎨 UI/UX Features

- Bold blue ASCII art logo
- Color-coded menu (bold green)
- Styled user prompts
- Success messages in bold green
- Error messages in bold yellow
- Exit message in bold red
- Automatic screen clearing after operations for clean transitions

---

## 🐛 Known Issues / TODO

- [ ] `viewTasks()` function not implemented
- [ ] `deleteTask()` function not implemented
- [ ] No input validation for date format
- [ ] No input validation for priority values
- [ ] `re` module imported but unused
- [ ] No error handling for missing CSV file on first read
- [ ] Hard-coded file path `../data/tasks.csv`

---

## 📊 Development Progress

**Overall Completion**: ~40%

| Component      | Status     | Completion |
| -------------- | ---------- | ---------- |
| Core Setup     | ✅ Done    | 100%       |
| UI/Console     | ✅ Done    | 100%       |
| Add Task       | ✅ Done    | 100%       |
| View Tasks     | 🚧 Pending | 0%         |
| Delete Task    | 🚧 Pending | 0%         |
| Edit Task      | ⏸️ Planned | 0%         |
| Validation     | ⏸️ Planned | 0%         |
| Error Handling | ⏸️ Planned | 0%         |

---

## 🚀 Next Steps

1. Implement `viewTasks()` function with colored output for priorities
2. Implement `deleteTask()` function with confirmation prompt
3. Add input validation for dates and priority levels
4. Implement error handling for file operations
5. Add task editing functionality
6. Create comprehensive test suite

---

## 📝 Notes

- Application uses cross-platform screen clearing (Windows: `cls`, Unix: `clear`)
- CSV file is created with headers on first write operation
- Task numbers are auto-incremented based on the last task in the file
- 2-second delay after adding tasks provides user feedback before screen clear

---

**Last Updated**: November 24, 2025

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
ToDo/
├── data/
│   └── tasks.csv     # Sample task data
├── src/
│   └── main.py       # Complete application with all functions
├── README.md         # This documentation
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

- [ ] Add task editing functionality
- [ ] Add task filtering by status/priority
- [ ] Add task search functionality
- [ ] Add recurring tasks feature
- [ ] Add task categories/tags
- [ ] Implement data backup functionality

---

## 📊 Development Progress

**Overall Completion**: ~95%

| Component      | Status  | Completion |
| -------------- | ------- | ---------- |
| Core Setup     | ✅ Done | 100%       |
| UI/Console     | ✅ Done | 100%       |
| Add Task       | ✅ Done | 100%       |
| View Tasks     | ✅ Done | 100%       |
| Delete Task    | ✅ Done | 100%       |
| Update Task    | ✅ Done | 100%       |
| CSV Export     | ✅ Done | 100%       |
| CSV Import     | ✅ Done | 100%       |
| Error Handling | ✅ Done | 100%       |

---

## 🚀 Future Enhancements

1. Add task editing functionality
2. Implement task search and filtering
3. Add recurring tasks support
4. Create task categories/tags system
5. Add data backup and restore features
6. Implement task reminders/notifications
7. Create comprehensive test suite

---

## 📝 Notes

- Application uses MySQL for robust data persistence
- Configuration is saved securely using pickle
- First-run wizard makes setup easy
- Urgency color-coding helps prioritize tasks visually
- CSV export/import enables data portability
- Screen clearing provides clean, professional UX

---

**Last Updated**: January 1, 2026

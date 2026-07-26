# Advanced Employee Management System

A Flask + SQLite Employee Management System extended from the provided Flask Development project. The application keeps the existing CRUD functionality and adds advanced employee data management features required by the assignment.

## Features

### Employee Management
- Create, view, update and delete employees
- Employee detail/profile page

### Department Management
- Create, view, update and delete departments
- Standalone department module (does not affect employee data)

### Advanced Search & Data Features
- Pagination with 5 or 10 records per page
- Previous/Next controls and numbered page links
- Search by employee name, email or department
- Sort by name, email, department or salary (ascending or descending)
- Filter by department (dropdown auto-populated from database)
- Filter by minimum and maximum salary range
- Search, filtering, sorting and pagination all work together without losing selected parameters
- Success/error flash messages and empty-result messages on all operations

### UI & Design
- Responsive Bootstrap 5.3 layout
- Glassmorphism card design with frosted glass effect
- Soft ambient gradient background
- Fade-in page load animations
- Hover-scale effect on cards and buttons
- Bootstrap Tooltips on all action buttons
- Live dashboard showing real-time employee and department counts

## Project Structure

```text
app/
├── models/
│   ├── __init__.py          # SQLAlchemy db instance
│   ├── employee.py          # Employee model
│   └── department.py        # Department model
├── routes/
│   ├── home.py              # Dashboard route
│   ├── employee.py          # Employee CRUD routes (search, filter, sort, pagination)
│   └── department.py        # Department CRUD routes
├── static/
│   └── css/
│       └── style.css        # Custom animations and styling
├── templates/
│   ├── base.html            # Base layout with navbar and footer
│   ├── navbar.html          # Navigation bar
│   ├── home.html            # Dashboard with live counts
│   ├── employee.html        # Employee list (search, filter, sort, pagination)
│   ├── add_employee.html    # Add employee form
│   ├── update_employee.html # Edit employee form
│   ├── employee_detail.html # Employee profile view
│   ├── department.html      # Department list
│   ├── add_department.html  # Add department form
│   └── update_department.html # Edit department form
└── __init__.py              # App factory (create_app)
migrations/
app.py                       # Application entry point
config.py                    # Configuration (DB URI, Secret Key)
requirements.txt             # Python dependencies
README.md
```

## Requirements

- Python 3.11+
- pip

> **No external database required.** This application uses **SQLite**, which is built into Python. The database file is created automatically on first run.

## Installation and Run

### Windows

```bash
python -m venv myvenv
myvenv\Scripts\activate
pip install -r requirements.txt
python app.py
```

### Linux/macOS

```bash
python3 -m venv myvenv
source myvenv/bin/activate
pip install -r requirements.txt
python app.py
```

Open the application at `http://127.0.0.1:5000`

## Database Setup

No manual database setup is required. The application uses **SQLite**. The database file (`employee.db`) is automatically created when the app starts for the first time.

The database connection in `config.py` is:

```python
SQLALCHEMY_DATABASE_URI = "sqlite:///employee.db"
```

To manually create or recreate the tables, run the following from a Flask shell:

```python
from app import create_app
from app.models import db
app = create_app()
with app.app_context():
    db.create_all()
```

## Key Routes

| Route | Description |
|-------|-------------|
| `/` or `/home` | Dashboard with live employee & department counts |
| `/employee/list` | Employee list with search, filter, sort & pagination |
| `/employee/add` | Add a new employee |
| `/employee/employeeUpdate/<id>` | Edit an existing employee |
| `/employee/employeeDelete/<id>` | Delete an employee |
| `/employee/employeeDetail/<id>` | View employee profile |
| `/department` | Department list |
| `/department/add` | Add a new department |
| `/department/update/<id>` | Edit a department |
| `/department/delete/<id>` | Delete a department |

## Assignment Verification

Before submission, verify CRUD, pagination, search, all sorting options, department filtering, salary range filtering, combined query behavior, responsive UI, and flash messages. Then push the latest project to your GitHub repository and submit that repository URL.

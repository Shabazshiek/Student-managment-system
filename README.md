# 🎓 EduTrack — Student Management System

A full-stack Django web application for managing student records, attendance, marks, departments, and reports.

---

## 🚀 Quick Start (Automatic)

```bash
python setup.py
python manage.py runserver
```

Then open: **http://127.0.0.1:8000/**  
Login: **admin** / **admin123**

---

## 🛠️ Manual Setup

### 1. Requirements
- Python 3.8 or higher
- pip

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Database Setup
```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Create Admin User
```bash
python manage.py createsuperuser
```
Or use the seed command which auto-creates `admin / admin123`:
```bash
python manage.py seed_data
```

### 5. Run the Server
```bash
python manage.py runserver
```

Visit **http://127.0.0.1:8000/**

---

## 📁 Project Structure

```
sms/
├── manage.py                   # Django management script
├── setup.py                    # One-click setup
├── requirements.txt            # Python dependencies
├── db.sqlite3                  # SQLite database (auto-created)
│
├── sms_project/                # Django project config
│   ├── settings.py             # Settings (DB, apps, templates)
│   ├── urls.py                 # Root URL config
│   └── wsgi.py
│
├── students/                   # Main application
│   ├── models.py               # DB models: Student, Department, Subject, Attendance, Marks
│   ├── views.py                # All page views and logic
│   ├── urls.py                 # App URL routes
│   ├── forms.py                # Django forms
│   ├── admin.py                # Django admin configuration
│   ├── context_processors.py   # Global template variables
│   ├── management/
│   │   └── commands/
│   │       └── seed_data.py    # Sample data seeder
│   └── templates/
│       └── students/
│           ├── login.html
│           ├── dashboard.html
│           ├── student_list.html
│           ├── student_form.html
│           ├── student_detail.html
│           ├── confirm_delete.html
│           ├── attendance.html
│           ├── marks.html
│           ├── departments.html
│           ├── subjects.html
│           └── reports.html
│
└── templates/
    └── base.html               # Shared layout with sidebar
```

---

## ✨ Features

| Feature | Details |
|---|---|
| **Login System** | Django auth, admin-only access |
| **Dashboard** | Stats cards, Chart.js graphs (grades, departments, attendance trend) |
| **Student CRUD** | Add, edit, view, delete students with photo upload |
| **Search & Filter** | By name, roll number, department, year, status |
| **Attendance** | Mark present/absent per student/subject/date, summary stats |
| **Marks & Grades** | Per-subject marks, auto grade (A+/A/B/C/D/F), percentage |
| **Departments** | Create and manage departments |
| **Subjects** | Assign subjects to departments |
| **Reports** | Full student report with attendance bar and grade |
| **CSV Export** | Download all student data as CSV |
| **Django Admin** | Full admin panel at /admin/ |

---

## 🗄️ Database Models

- **Student** — roll_number, name, email, phone, gender, dob, department, year, address, photo, status
- **Department** — name, code, description
- **Subject** — name, code, department, max_marks, credits
- **Attendance** — student, date, status (present/absent/leave), subject, marked_by
- **Marks** — student, subject, exam_type, marks_obtained, max_marks, exam_date

---

## 🔧 Tech Stack

- **Backend:** Python 3.x + Django 4.2
- **Frontend:** HTML5, CSS3, Bootstrap 5, Chart.js
- **Database:** SQLite (default) — switch to PostgreSQL in settings.py
- **Auth:** Django built-in authentication

---

## 🔁 Switch to PostgreSQL

In `sms_project/settings.py`, replace the DATABASES section:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'sms_db',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

Then: `pip install psycopg2-binary`

---

## 📜 URL Routes

| URL | View |
|---|---|
| `/` | Dashboard |
| `/login/` | Login |
| `/students/` | Student list |
| `/students/add/` | Add student |
| `/students/<id>/` | Student profile |
| `/students/<id>/edit/` | Edit student |
| `/students/<id>/delete/` | Delete student |
| `/attendance/` | Attendance tracker |
| `/marks/` | Marks & Grades |
| `/departments/` | Departments |
| `/subjects/` | Subjects |
| `/reports/` | Reports |
| `/reports/export/` | CSV export |
| `/admin/` | Django Admin |

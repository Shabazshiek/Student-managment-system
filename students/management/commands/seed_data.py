"""
Management command to seed the database with sample data.
Run with: python manage.py seed_data
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from students.models import Department, Student, Subject, Attendance, Marks
from datetime import date, timedelta
import random


class Command(BaseCommand):
    help = 'Seeds the database with sample departments, subjects, and students'

    def handle(self, *args, **kwargs):
        self.stdout.write('🌱 Seeding database...')

        # Create superuser
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@edutrack.com', 'admin123')
            self.stdout.write(self.style.SUCCESS('  ✓ Admin user created (admin / admin123)'))

        # Departments
        depts_data = [
            ('Computer Science', 'CS', 'Programming, algorithms, and software engineering'),
            ('Mathematics', 'MATH', 'Pure and applied mathematics'),
            ('Physics', 'PHY', 'Classical and modern physics'),
            ('Chemistry', 'CHEM', 'Organic and inorganic chemistry'),
            ('Biology', 'BIO', 'Life sciences and biotechnology'),
            ('Engineering', 'ENG', 'Mechanical and electrical engineering'),
        ]
        departments = {}
        for name, code, desc in depts_data:
            dept, created = Department.objects.get_or_create(
                code=code, defaults={'name': name, 'description': desc}
            )
            departments[code] = dept
            if created:
                self.stdout.write(f'  ✓ Department: {name}')

        # Subjects per department
        subjects_data = {
            'CS': [('Data Structures', 'CS101'), ('Algorithms', 'CS102'), ('Database Systems', 'CS103'), ('Web Development', 'CS104')],
            'MATH': [('Calculus', 'MATH101'), ('Linear Algebra', 'MATH102'), ('Statistics', 'MATH103')],
            'PHY': [('Mechanics', 'PHY101'), ('Electromagnetism', 'PHY102'), ('Quantum Physics', 'PHY103')],
            'CHEM': [('Organic Chemistry', 'CHEM101'), ('Inorganic Chemistry', 'CHEM102')],
            'BIO': [('Cell Biology', 'BIO101'), ('Genetics', 'BIO102'), ('Ecology', 'BIO103')],
            'ENG': [('Engineering Mechanics', 'ENG101'), ('Thermodynamics', 'ENG102'), ('Circuit Theory', 'ENG103')],
        }
        subjects = {}
        for dept_code, subs in subjects_data.items():
            dept = departments[dept_code]
            for name, code in subs:
                sub, created = Subject.objects.get_or_create(
                    code=code, defaults={'name': name, 'department': dept, 'max_marks': 100, 'credits': 3}
                )
                subjects[code] = sub
                if created:
                    self.stdout.write(f'  ✓ Subject: {name}')

        # Students
        students_data = [
            ('Arjun', 'Sharma', '2024001', 'CS', 'M', 1, 'arjun@example.com'),
            ('Priya', 'Patel', '2024002', 'CS', 'F', 1, 'priya@example.com'),
            ('Rahul', 'Kumar', '2024003', 'MATH', 'M', 2, 'rahul@example.com'),
            ('Ananya', 'Singh', '2024004', 'PHY', 'F', 2, 'ananya@example.com'),
            ('Vikram', 'Reddy', '2024005', 'CHEM', 'M', 3, 'vikram@example.com'),
            ('Meera', 'Nair', '2024006', 'BIO', 'F', 3, 'meera@example.com'),
            ('Siddharth', 'Joshi', '2024007', 'ENG', 'M', 4, 'siddharth@example.com'),
            ('Kavya', 'Gupta', '2024008', 'CS', 'F', 4, 'kavya@example.com'),
            ('Rohan', 'Mehta', '2024009', 'MATH', 'M', 1, 'rohan@example.com'),
            ('Sneha', 'Iyer', '2024010', 'PHY', 'F', 2, 'sneha@example.com'),
            ('Aditya', 'Verma', '2024011', 'CS', 'M', 3, 'aditya@example.com'),
            ('Pooja', 'Rao', '2024012', 'BIO', 'F', 1, 'pooja@example.com'),
        ]

        admin_user = User.objects.get(username='admin')
        created_students = []

        for fname, lname, roll, dept_code, gender, year, email in students_data:
            student, created = Student.objects.get_or_create(
                roll_number=roll,
                defaults={
                    'first_name': fname, 'last_name': lname,
                    'email': email, 'phone': f'+91 98765 {random.randint(10000,99999)}',
                    'gender': gender, 'department': departments[dept_code],
                    'year': year, 'status': 'active',
                    'address': f'{random.randint(1,200)}, Sample Street, City',
                    'date_of_birth': date(2002 - year, random.randint(1,12), random.randint(1,28)),
                }
            )
            created_students.append(student)
            if created:
                self.stdout.write(f'  ✓ Student: {fname} {lname}')

        # Attendance (last 30 days)
        att_count = 0
        for student in created_students:
            for i in range(30):
                att_date = date.today() - timedelta(days=i)
                if att_date.weekday() < 5:  # Weekdays only
                    status = 'present' if random.random() > 0.15 else 'absent'
                    Attendance.objects.get_or_create(
                        student=student, date=att_date, subject=None,
                        defaults={'status': status, 'marked_by': admin_user}
                    )
                    att_count += 1

        self.stdout.write(f'  ✓ {att_count} attendance records created')

        # Marks
        exam_types = ['midterm', 'final', 'assignment']
        marks_count = 0
        for student in created_students:
            dept_code = student.department.code if student.department else 'CS'
            dept_subjects = list(Subject.objects.filter(department=student.department))
            if not dept_subjects:
                continue
            for subject in dept_subjects:
                for exam in exam_types:
                    score = random.randint(45, 98)
                    Marks.objects.get_or_create(
                        student=student, subject=subject, exam_type=exam,
                        defaults={
                            'marks_obtained': score, 'max_marks': 100,
                            'exam_date': date.today() - timedelta(days=random.randint(10, 60)),
                            'entered_by': admin_user
                        }
                    )
                    marks_count += 1

        self.stdout.write(f'  ✓ {marks_count} marks records created')
        self.stdout.write(self.style.SUCCESS('\n✅ Database seeded successfully!'))
        self.stdout.write(self.style.SUCCESS('   Login: admin / admin123'))
        self.stdout.write(self.style.SUCCESS('   URL: http://127.0.0.1:8000/'))

from django.db import models
from django.contrib.auth.models import User


class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=10, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Student(models.Model):
    GENDER_CHOICES = [('M', 'Male'), ('F', 'Female'), ('O', 'Other')]
    YEAR_CHOICES = [(1, 'Year 1'), (2, 'Year 2'), (3, 'Year 3'), (4, 'Year 4')]
    STATUS_CHOICES = [('active', 'Active'), ('inactive', 'Inactive'), ('graduated', 'Graduated')]

    roll_number = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='M')
    date_of_birth = models.DateField(null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, related_name='students')
    year = models.IntegerField(choices=YEAR_CHOICES, default=1)
    address = models.TextField(blank=True)
    photo = models.FileField(upload_to='students/', null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    admission_date = models.DateField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.roll_number})"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_attendance_percentage(self):
        total = self.attendances.count()
        if total == 0:
            return 0
        present = self.attendances.filter(status='present').count()
        return round((present / total) * 100, 1)

    def get_average_marks(self):
        marks = self.marks.all()
        if not marks.exists():
            return 0
        total = sum(m.marks_obtained for m in marks)
        return round(total / marks.count(), 1)

    def get_grade(self):
        avg = self.get_average_marks()
        if avg >= 85: return 'A+'
        elif avg >= 75: return 'A'
        elif avg >= 65: return 'B'
        elif avg >= 55: return 'C'
        elif avg >= 40: return 'D'
        else: return 'F'

    class Meta:
        ordering = ['roll_number']


class Subject(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='subjects')
    max_marks = models.IntegerField(default=100)
    credits = models.IntegerField(default=3)

    def __str__(self):
        return f"{self.name} ({self.code})"

    class Meta:
        ordering = ['name']


class Attendance(models.Model):
    STATUS_CHOICES = [('present', 'Present'), ('absent', 'Absent'), ('leave', 'Leave')]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='present')
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, blank=True)
    remarks = models.CharField(max_length=200, blank=True)
    marked_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} - {self.date} - {self.status}"

    class Meta:
        unique_together = ['student', 'date', 'subject']
        ordering = ['-date']


class Marks(models.Model):
    EXAM_CHOICES = [
        ('midterm', 'Mid Term'),
        ('final', 'Final Exam'),
        ('assignment', 'Assignment'),
        ('quiz', 'Quiz'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='marks')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='marks')
    exam_type = models.CharField(max_length=20, choices=EXAM_CHOICES, default='final')
    marks_obtained = models.FloatField(default=0)
    max_marks = models.FloatField(default=100)
    exam_date = models.DateField(null=True, blank=True)
    remarks = models.CharField(max_length=200, blank=True)
    entered_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_percentage(self):
        if self.max_marks == 0:
            return 0
        return round((self.marks_obtained / self.max_marks) * 100, 1)

    def get_grade(self):
        pct = self.get_percentage()
        if pct >= 85: return 'A+'
        elif pct >= 75: return 'A'
        elif pct >= 65: return 'B'
        elif pct >= 55: return 'C'
        elif pct >= 40: return 'D'
        else: return 'F'

    def __str__(self):
        return f"{self.student} - {self.subject} - {self.marks_obtained}"

    class Meta:
        unique_together = ['student', 'subject', 'exam_type']
        ordering = ['-created_at']

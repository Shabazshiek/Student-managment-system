from django.contrib import admin
from .models import Student, Department, Subject, Attendance, Marks

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'code']
    search_fields = ['name', 'code']

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['roll_number', 'first_name', 'last_name', 'department', 'year', 'status']
    list_filter = ['department', 'year', 'status', 'gender']
    search_fields = ['roll_number', 'first_name', 'last_name', 'email']

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'department', 'max_marks', 'credits']
    list_filter = ['department']

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['student', 'date', 'status', 'subject']
    list_filter = ['status', 'date']
    search_fields = ['student__first_name', 'student__last_name']

@admin.register(Marks)
class MarksAdmin(admin.ModelAdmin):
    list_display = ['student', 'subject', 'exam_type', 'marks_obtained', 'max_marks']
    list_filter = ['exam_type', 'subject']

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count, Avg
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
import csv
import json
from datetime import date, timedelta

from .models import Student, Department, Subject, Attendance, Marks
from .forms import (LoginForm, StudentForm, DepartmentForm,
                    SubjectForm, AttendanceForm, MarksForm, StudentSearchForm)


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    form = LoginForm(request, data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.get_full_name() or user.username}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'students/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('login')


@login_required
def dashboard(request):
    total_students = Student.objects.count()
    active_students = Student.objects.filter(status='active').count()
    total_departments = Department.objects.count()
    total_subjects = Subject.objects.count()

    # Attendance stats
    today = date.today()
    today_attendance = Attendance.objects.filter(date=today)
    today_present = today_attendance.filter(status='present').count()

    # Grade distribution
    grade_dist = {'A+': 0, 'A': 0, 'B': 0, 'C': 0, 'D': 0, 'F': 0}
    for s in Student.objects.all():
        g = s.get_grade()
        if g in grade_dist:
            grade_dist[g] += 1

    # Department wise students
    dept_data = Department.objects.annotate(student_count=Count('students')).values('name', 'student_count')

    # Recent students
    recent_students = Student.objects.select_related('department').order_by('-created_at')[:8]

    # Monthly attendance trend (last 7 days)
    att_trend = []
    for i in range(6, -1, -1):
        d = today - timedelta(days=i)
        total = Attendance.objects.filter(date=d).count()
        present = Attendance.objects.filter(date=d, status='present').count()
        pct = round((present / total * 100), 1) if total > 0 else 0
        att_trend.append({'date': d.strftime('%b %d'), 'pct': pct})

    context = {
        'total_students': total_students,
        'active_students': active_students,
        'total_departments': total_departments,
        'total_subjects': total_subjects,
        'today_present': today_present,
        'grade_dist': json.dumps(grade_dist),
        'dept_data': json.dumps(list(dept_data)),
        'recent_students': recent_students,
        'att_trend': json.dumps(att_trend),
    }
    return render(request, 'students/dashboard.html', context)


@login_required
def student_list(request):
    form = StudentSearchForm(request.GET)
    students = Student.objects.select_related('department').all()

    if form.is_valid():
        q = form.cleaned_data.get('query')
        dept = form.cleaned_data.get('department')
        year = form.cleaned_data.get('year')
        status = form.cleaned_data.get('status')

        if q:
            students = students.filter(
                Q(first_name__icontains=q) | Q(last_name__icontains=q) |
                Q(roll_number__icontains=q) | Q(email__icontains=q)
            )
        if dept:
            students = students.filter(department=dept)
        if year:
            students = students.filter(year=year)
        if status:
            students = students.filter(status=status)

    context = {
        'students': students,
        'form': form,
        'total': students.count(),
    }
    return render(request, 'students/student_list.html', context)


@login_required
def student_add(request):
    form = StudentForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        if form.is_valid():
            student = form.save()
            messages.success(request, f'Student {student.get_full_name()} added successfully!')
            return redirect('student_list')
        else:
            messages.error(request, 'Please fix the errors below.')
    return render(request, 'students/student_form.html', {'form': form, 'title': 'Add New Student', 'action': 'Add'})


@login_required
def student_edit(request, pk):
    student = get_object_or_404(Student, pk=pk)
    form = StudentForm(request.POST or None, request.FILES or None, instance=student)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, f'Student {student.get_full_name()} updated successfully!')
            return redirect('student_detail', pk=pk)
        else:
            messages.error(request, 'Please fix the errors below.')
    return render(request, 'students/student_form.html', {'form': form, 'title': 'Edit Student', 'action': 'Update', 'student': student})


@login_required
def student_detail(request, pk):
    student = get_object_or_404(Student, pk=pk)
    attendances = student.attendances.order_by('-date')[:20]
    marks = student.marks.select_related('subject').all()
    context = {
        'student': student,
        'attendances': attendances,
        'marks': marks,
        'att_pct': student.get_attendance_percentage(),
        'avg_marks': student.get_average_marks(),
        'grade': student.get_grade(),
    }
    return render(request, 'students/student_detail.html', context)


@login_required
def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        name = student.get_full_name()
        student.delete()
        messages.success(request, f'Student {name} deleted successfully!')
        return redirect('student_list')
    return render(request, 'students/confirm_delete.html', {'student': student})


@login_required
def attendance_list(request):
    attendances = Attendance.objects.select_related('student', 'subject').order_by('-date')[:100]
    form = AttendanceForm(request.POST or None, initial={'date': date.today()})
    if request.method == 'POST':
        if form.is_valid():
            att = form.save(commit=False)
            att.marked_by = request.user
            # Check for existing record
            existing = Attendance.objects.filter(
                student=att.student, date=att.date, subject=att.subject
            ).first()
            if existing:
                existing.status = att.status
                existing.remarks = att.remarks
                existing.save()
                messages.success(request, 'Attendance updated!')
            else:
                att.save()
                messages.success(request, 'Attendance marked successfully!')
            return redirect('attendance_list')
        else:
            messages.error(request, 'Please fix errors.')

    # Summary stats
    today = date.today()
    today_total = Attendance.objects.filter(date=today).count()
    today_present = Attendance.objects.filter(date=today, status='present').count()

    context = {
        'attendances': attendances,
        'form': form,
        'today_total': today_total,
        'today_present': today_present,
    }
    return render(request, 'students/attendance.html', context)


@login_required
def marks_list(request):
    marks = Marks.objects.select_related('student', 'subject').order_by('-created_at')
    form = MarksForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            mark = form.save(commit=False)
            mark.entered_by = request.user
            existing = Marks.objects.filter(
                student=mark.student, subject=mark.subject, exam_type=mark.exam_type
            ).first()
            if existing:
                existing.marks_obtained = mark.marks_obtained
                existing.max_marks = mark.max_marks
                existing.exam_date = mark.exam_date
                existing.remarks = mark.remarks
                existing.save()
                messages.success(request, 'Marks updated!')
            else:
                mark.save()
                messages.success(request, 'Marks added successfully!')
            return redirect('marks_list')
        else:
            messages.error(request, 'Please fix errors.')

    context = {'marks': marks, 'form': form}
    return render(request, 'students/marks.html', context)


@login_required
def department_list(request):
    departments = Department.objects.annotate(
        student_count=Count('students'),
        subject_count=Count('subjects')
    ).all()
    form = DepartmentForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Department added!')
            return redirect('department_list')
    return render(request, 'students/departments.html', {'departments': departments, 'form': form})


@login_required
def department_delete(request, pk):
    dept = get_object_or_404(Department, pk=pk)
    if request.method == 'POST':
        dept.delete()
        messages.success(request, f'Department {dept.name} deleted.')
        return redirect('department_list')
    return redirect('department_list')


@login_required
def subject_list(request):
    subjects = Subject.objects.select_related('department').all()
    form = SubjectForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Subject added!')
            return redirect('subject_list')
    return render(request, 'students/subjects.html', {'subjects': subjects, 'form': form})


@login_required
def reports(request):
    students = Student.objects.select_related('department').all()
    report_data = []
    for s in students:
        report_data.append({
            'student': s,
            'att_pct': s.get_attendance_percentage(),
            'avg_marks': s.get_average_marks(),
            'grade': s.get_grade(),
        })
    context = {'report_data': report_data}
    return render(request, 'students/reports.html', context)


@login_required
def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="students_report.csv"'
    writer = csv.writer(response)
    writer.writerow(['Roll No', 'Name', 'Department', 'Year', 'Email', 'Phone', 'Status', 'Attendance %', 'Avg Marks', 'Grade'])
    for s in Student.objects.select_related('department').all():
        writer.writerow([
            s.roll_number, s.get_full_name(), s.department.name if s.department else '',
            s.get_year_display(), s.email, s.phone, s.status,
            s.get_attendance_percentage(), s.get_average_marks(), s.get_grade()
        ])
    return response


@login_required
def api_attendance_stats(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    total = student.attendances.count()
    present = student.attendances.filter(status='present').count()
    absent = student.attendances.filter(status='absent').count()
    return JsonResponse({
        'total': total, 'present': present, 'absent': absent,
        'percentage': student.get_attendance_percentage()
    })

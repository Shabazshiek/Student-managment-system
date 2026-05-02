from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Students
    path('students/', views.student_list, name='student_list'),
    path('students/add/', views.student_add, name='student_add'),
    path('students/<int:pk>/', views.student_detail, name='student_detail'),
    path('students/<int:pk>/edit/', views.student_edit, name='student_edit'),
    path('students/<int:pk>/delete/', views.student_delete, name='student_delete'),

    # Attendance
    path('attendance/', views.attendance_list, name='attendance_list'),

    # Marks
    path('marks/', views.marks_list, name='marks_list'),

    # Departments & Subjects
    path('departments/', views.department_list, name='department_list'),
    path('departments/<int:pk>/delete/', views.department_delete, name='department_delete'),
    path('subjects/', views.subject_list, name='subject_list'),

    # Reports
    path('reports/', views.reports, name='reports'),
    path('reports/export/', views.export_csv, name='export_csv'),

    # API
    path('api/attendance/<int:student_id>/', views.api_attendance_stats, name='api_attendance_stats'),
]

from .models import Student

def global_context(request):
    return {
        'total_students_count': Student.objects.count()
    }

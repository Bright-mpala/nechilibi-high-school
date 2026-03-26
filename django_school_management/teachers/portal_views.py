from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django_school_management.teachers.models import Teacher
from permission_handlers.basic import user_is_teacher


@login_required
def teacher_dashboard(request):
    """Teacher's personal dashboard."""
    teacher_id = request.user.employee_or_student_id
    if not teacher_id or not user_is_teacher(request.user):
        messages.error(request, 'No teacher profile linked to your account.')
        return redirect('/')

    try:
        teacher = Teacher.objects.select_related('designation', 'institute').get(
            employee_id=teacher_id
        )
    except Teacher.DoesNotExist:
        messages.error(request, 'Teacher record not found.')
        return redirect('/')

    context = {
        'teacher': teacher,
        'page_title': 'Teacher Dashboard',
    }

    # Subjects where this teacher is the instructor
    try:
        from django_school_management.academics.models import Subject
        context['subjects'] = Subject.objects.filter(instructor=teacher).order_by('name')
    except Exception:
        context['subjects'] = []

    # Total student count
    try:
        from django_school_management.students.models import Student
        context['student_count'] = Student.objects.count()
    except Exception:
        context['student_count'] = 0

    return render(request, 'portal/teacher/dashboard.html', context)


@login_required
def teacher_profile(request):
    """Teacher profile page."""
    teacher_id = request.user.employee_or_student_id
    if not teacher_id or not user_is_teacher(request.user):
        messages.error(request, 'No teacher profile linked to your account.')
        return redirect('/')

    try:
        teacher = Teacher.objects.select_related('designation', 'institute').get(
            employee_id=teacher_id
        )
    except Teacher.DoesNotExist:
        messages.error(request, 'Teacher record not found.')
        return redirect('/')

    return render(request, 'portal/teacher/profile.html', {
        'teacher': teacher,
        'page_title': 'My Profile',
    })

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django_school_management.students.models import Student
from permission_handlers.basic import user_is_student


@login_required
def student_dashboard(request):
    """Student's personal dashboard."""
    student_id = request.user.employee_or_student_id
    if not student_id or not user_is_student(request.user):
        messages.error(request, 'No student profile linked to your account.')
        return redirect('/')

    try:
        student = Student.objects.select_related(
            'admission_student',
            'admission_student__choosen_department',
            'semester',
            'batch',
            'ac_session',
        ).get(temporary_id=student_id)
    except Student.DoesNotExist:
        messages.error(request, 'Student record not found.')
        return redirect('/')

    context = {
        'student': student,
        'page_title': 'Student Dashboard',
    }

    # Try to get results
    try:
        from django_school_management.result.models import Result
        results = Result.objects.filter(student=student).select_related('subject', 'semester', 'exam')
        context['results'] = results
    except Exception:
        context['results'] = []

    # Try to get current academic session
    try:
        from django_school_management.academics.models import AcademicSession
        current_session = student.ac_session
        context['current_session'] = current_session
    except Exception:
        context['current_session'] = None

    # Try to get subjects for student's semester/department
    try:
        from django_school_management.result.models import SubjectGroup
        department = student.admission_student.choosen_department
        subject_group = SubjectGroup.objects.filter(
            department=department, semester=student.semester
        ).first()
        context['subjects'] = subject_group.subjects.all() if subject_group else []
    except Exception:
        context['subjects'] = []

    return render(request, 'portal/student/dashboard.html', context)


@login_required
def student_results(request):
    """Student results page."""
    student_id = request.user.employee_or_student_id
    if not student_id or not user_is_student(request.user):
        messages.error(request, 'No student profile linked to your account.')
        return redirect('/')

    try:
        student = Student.objects.select_related(
            'admission_student',
            'admission_student__choosen_department',
            'semester',
        ).get(temporary_id=student_id)
    except Student.DoesNotExist:
        messages.error(request, 'Student record not found.')
        return redirect('/')

    context = {'student': student, 'page_title': 'My Results'}

    try:
        from django_school_management.result.models import Result
        context['results'] = Result.objects.filter(student=student).select_related(
            'subject', 'semester', 'exam'
        ).order_by('semester__number', 'subject__name')
    except Exception:
        context['results'] = []

    return render(request, 'portal/student/results.html', context)


@login_required
def student_profile(request):
    """Student profile page."""
    student_id = request.user.employee_or_student_id
    if not student_id or not user_is_student(request.user):
        messages.error(request, 'No student profile linked to your account.')
        return redirect('/')

    try:
        student = Student.objects.select_related(
            'admission_student',
            'admission_student__choosen_department',
            'semester',
            'batch',
        ).get(temporary_id=student_id)
    except Student.DoesNotExist:
        messages.error(request, 'Student record not found.')
        return redirect('/')

    return render(request, 'portal/student/profile.html', {
        'student': student,
        'page_title': 'My Profile',
    })

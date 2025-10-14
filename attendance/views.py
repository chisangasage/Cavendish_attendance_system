from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q
from django.utils import timezone
from django import forms
from django.http import HttpResponseForbidden
from functools import wraps
from datetime import datetime, timedelta
from .models import UserProfile, Course, Enrollment, AttendanceSession, AttendanceRecord
from .forms import (UserRegistrationForm, CourseForm, EnrollmentForm, 
                    AttendanceSessionForm, AttendanceMarkingForm, AttendanceFilterForm)
from django.contrib.auth.models import User

def lecturer_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        
        try:
            if request.user.profile.role != 'lecturer':
                messages.error(request, 'Access denied. Only lecturers can access this page.')
                return HttpResponseForbidden('Access denied. Only lecturers can access this page.')
        except UserProfile.DoesNotExist:
            messages.error(request, 'Profile not found. Please contact administrator.')
            return redirect('dashboard')
        
        return view_func(request, *args, **kwargs)
    return wrapper

def student_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        
        try:
            if request.user.profile.role != 'student':
                messages.error(request, 'Access denied. Only students can access this page.')
                return HttpResponseForbidden('Access denied. Only students can access this page.')
        except UserProfile.DoesNotExist:
            messages.error(request, 'Profile not found. Please contact administrator.')
            return redirect('dashboard')
        
        return view_func(request, *args, **kwargs)
    return wrapper
"""
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(
                user=user,
                role=form.cleaned_data['role'],
                student_id=form.cleaned_data.get('student_id'),
                phone=form.cleaned_data.get('phone')
            )
            messages.success(request, 'Account created successfully! You can now login.')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'attendance/register.html', {'form': form})
"""

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'attendance/login.html')

@login_required
def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')

@login_required
def dashboard(request):
    try:
        user_profile = request.user.profile
    except UserProfile.DoesNotExist:
        messages.error(request, 'Profile not found. Please complete your profile or contact administrator.')
        logout(request)
        return redirect('login')
    
    context = {'user_profile': user_profile}
    
    if user_profile.role == 'lecturer':
        courses = Course.objects.filter(lecturer=request.user)
        total_students = Enrollment.objects.filter(course__lecturer=request.user).count()
        total_sessions = AttendanceSession.objects.filter(created_by=request.user).count()
        
        recent_sessions = AttendanceSession.objects.filter(
            created_by=request.user
        ).order_by('-session_date', '-session_time')[:5]
        
        context.update({
            'courses': courses,
            'total_courses': courses.count(),
            'total_students': total_students,
            'total_sessions': total_sessions,
            'recent_sessions': recent_sessions,
        })
        return render(request, 'attendance/lecturer_dashboard.html', context)
    
    else:
        enrollments = Enrollment.objects.filter(student=request.user)
        total_courses = enrollments.count()
        
        attendance_stats = []
        for enrollment in enrollments:
            course = enrollment.course
            total_sessions = AttendanceSession.objects.filter(course=course).count()
            attended = AttendanceRecord.objects.filter(
                student=request.user,
                session__course=course,
                status='present'
            ).count()
            
            attendance_rate = (attended / total_sessions * 100) if total_sessions > 0 else 0
            
            attendance_stats.append({
                'course': course,
                'total_sessions': total_sessions,
                'attended': attended,
                'attendance_rate': round(attendance_rate, 1)
            })
        
        context.update({
            'enrollments': enrollments,
            'total_courses': total_courses,
            'attendance_stats': attendance_stats,
        })
        return render(request, 'attendance/student_dashboard.html', context)

@login_required
def course_list(request):
    try:
        user_role = request.user.profile.role
    except UserProfile.DoesNotExist:
        messages.error(request, 'Profile not found. Please contact administrator.')
        return redirect('dashboard')
    
    if user_role == 'lecturer':
        courses = Course.objects.filter(lecturer=request.user)
    else:
        enrollments = Enrollment.objects.filter(student=request.user)
        courses = [e.course for e in enrollments]
    
    return render(request, 'attendance/course_list.html', {'courses': courses})

@lecturer_required
def course_create(request):
    
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.lecturer = request.user
            course.save()
            messages.success(request, 'Course created successfully!')
            return redirect('course_list')
    else:
        form = CourseForm(initial={'lecturer': request.user})
        form.fields['lecturer'].widget = forms.HiddenInput()
    
    return render(request, 'attendance/course_form.html', {'form': form, 'title': 'Create Course'})

@lecturer_required
def course_edit(request, pk):
    course = get_object_or_404(Course, pk=pk, lecturer=request.user)
    
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, 'Course updated successfully!')
            return redirect('course_list')
    else:
        form = CourseForm(instance=course)
    
    return render(request, 'attendance/course_form.html', {'form': form, 'title': 'Edit Course'})

@lecturer_required
def course_delete(request, pk):
    course = get_object_or_404(Course, pk=pk, lecturer=request.user)
    
    if request.method == 'POST':
        course.delete()
        messages.success(request, 'Course deleted successfully!')
        return redirect('course_list')
    
    return render(request, 'attendance/course_confirm_delete.html', {'course': course})

@login_required
def enrollment_list(request):
    try:
        user_role = request.user.profile.role
    except UserProfile.DoesNotExist:
        messages.error(request, 'Profile not found. Please contact administrator.')
        return redirect('dashboard')
    
    if user_role == 'lecturer':
        enrollments = Enrollment.objects.filter(course__lecturer=request.user)
    else:
        enrollments = Enrollment.objects.filter(student=request.user)
    
    return render(request, 'attendance/enrollment_list.html', {'enrollments': enrollments})

@lecturer_required
def enrollment_create(request):
    
    if request.method == 'POST':
        form = EnrollmentForm(request.POST, lecturer=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student enrolled successfully!')
            return redirect('enrollment_list')
    else:
        form = EnrollmentForm(lecturer=request.user)
    
    return render(request, 'attendance/enrollment_form.html', {'form': form})

@lecturer_required
def attendance_session_create(request):
    
    if request.method == 'POST':
        form = AttendanceSessionForm(request.POST, lecturer=request.user)
        if form.is_valid():
            session = form.save(commit=False)
            session.created_by = request.user
            session.save()
            messages.success(request, 'Attendance session created successfully!')
            return redirect('attendance_mark', session_id=session.id)
    else:
        form = AttendanceSessionForm(lecturer=request.user)
    
    return render(request, 'attendance/session_form.html', {'form': form})

@lecturer_required
def attendance_mark(request, session_id):
    session = get_object_or_404(AttendanceSession, pk=session_id, created_by=request.user)
    enrolled_students = User.objects.filter(
        enrollments__course=session.course,
        profile__role='student'
    ).distinct()
    
    if request.method == 'POST':
        for student in enrolled_students:
            status = request.POST.get(f'status_{student.id}')
            remarks = request.POST.get(f'remarks_{student.id}', '')
            
            AttendanceRecord.objects.update_or_create(
                session=session,
                student=student,
                defaults={'status': status, 'remarks': remarks}
            )
        
        messages.success(request, 'Attendance marked successfully!')
        return redirect('attendance_session_list')
    
    existing_records = {
        record.student.id: record 
        for record in AttendanceRecord.objects.filter(session=session)
    }
    
    students_with_attendance = []
    for student in enrolled_students:
        record = existing_records.get(student.id)
        students_with_attendance.append({
            'student': student,
            'status': record.status if record else 'absent',
            'remarks': record.remarks if record else ''
        })
    
    context = {
        'session': session,
        'students': students_with_attendance,
    }
    
    return render(request, 'attendance/mark_attendance.html', context)

@login_required
def attendance_session_list(request):
    try:
        user_role = request.user.profile.role
    except UserProfile.DoesNotExist:
        messages.error(request, 'Profile not found. Please contact administrator.')
        return redirect('dashboard')
    
    if user_role == 'lecturer':
        sessions = AttendanceSession.objects.filter(created_by=request.user)
    else:
        sessions = AttendanceSession.objects.filter(
            course__enrollments__student=request.user
        ).distinct()
    
    return render(request, 'attendance/session_list.html', {'sessions': sessions})

@login_required
def attendance_records(request):
    try:
        user_role = request.user.profile.role
    except UserProfile.DoesNotExist:
        messages.error(request, 'Profile not found. Please contact administrator.')
        return redirect('dashboard')
    
    if user_role == 'student':
        records = AttendanceRecord.objects.filter(student=request.user).order_by('-session__session_date')
        courses = Course.objects.filter(enrollments__student=request.user)
        
        attendance_data = {}
        for course in courses:
            sessions = AttendanceSession.objects.filter(course=course).order_by('session_date')
            course_records = AttendanceRecord.objects.filter(
                student=request.user,
                session__course=course
            )
            
            dates = [s.session_date.strftime('%Y-%m-%d') for s in sessions]
            statuses = []
            
            for session in sessions:
                record = course_records.filter(session=session).first()
                if record:
                    statuses.append(1 if record.status == 'present' else 0)
                else:
                    statuses.append(0)
            
            if dates:
                attendance_data[course.course_code] = {
                    'dates': dates,
                    'statuses': statuses
                }
        
        context = {
            'records': records,
            'attendance_data': attendance_data,
        }
        return render(request, 'attendance/student_records.html', context)
    
    else:
        form = AttendanceFilterForm()
        records = AttendanceRecord.objects.filter(
            session__course__lecturer=request.user
        ).order_by('-session__session_date')
        
        if request.GET:
            form = AttendanceFilterForm(request.GET)
            if form.is_valid():
                if form.cleaned_data.get('course'):
                    records = records.filter(session__course=form.cleaned_data['course'])
                if form.cleaned_data.get('start_date'):
                    records = records.filter(session__session_date__gte=form.cleaned_data['start_date'])
                if form.cleaned_data.get('end_date'):
                    records = records.filter(session__session_date__lte=form.cleaned_data['end_date'])
                if form.cleaned_data.get('status'):
                    records = records.filter(status=form.cleaned_data['status'])
        
        context = {
            'records': records,
            'form': form,
        }
        return render(request, 'attendance/lecturer_records.html', context)

@lecturer_required
def reports(request):
    
    courses = Course.objects.filter(lecturer=request.user)
    selected_course = None
    report_data = []
    
    if request.GET.get('course'):
        selected_course = get_object_or_404(Course, pk=request.GET.get('course'), lecturer=request.user)
        students = User.objects.filter(
            enrollments__course=selected_course,
            profile__role='student'
        ).distinct()
        
        for student in students:
            total_sessions = AttendanceSession.objects.filter(course=selected_course).count()
            present_count = AttendanceRecord.objects.filter(
                student=student,
                session__course=selected_course,
                status='present'
            ).count()
            absent_count = AttendanceRecord.objects.filter(
                student=student,
                session__course=selected_course,
                status='absent'
            ).count()
            late_count = AttendanceRecord.objects.filter(
                student=student,
                session__course=selected_course,
                status='late'
            ).count()
            
            attendance_rate = (present_count / total_sessions * 100) if total_sessions > 0 else 0
            
            report_data.append({
                'student': student,
                'student_id': student.profile.student_id,
                'total_sessions': total_sessions,
                'present': present_count,
                'absent': absent_count,
                'late': late_count,
                'attendance_rate': round(attendance_rate, 1)
            })
    
    context = {
        'courses': courses,
        'selected_course': selected_course,
        'report_data': report_data,
    }
    
    return render(request, 'attendance/reports.html', context)

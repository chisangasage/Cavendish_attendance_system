from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class UserProfile(models.Model):
    ROLE_CHOICES = (
        ('lecturer', 'Lecturer'),
        ('student', 'Student'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    student_id = models.CharField(max_length=20, unique=True, null=True, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.role}"
    
    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'


class Course(models.Model):
    course_code = models.CharField(max_length=20, unique=True)
    course_name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    lecturer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses_taught', limit_choices_to={'profile__role': 'lecturer'})
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.course_code} - {self.course_name}"
    
    def get_total_sessions(self):
        return self.attendance_sessions.count()
    
    def get_enrolled_students_count(self):
        return self.enrollments.count()
    
    class Meta:
        ordering = ['course_code']
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'


class Enrollment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments', limit_choices_to={'profile__role': 'student'})
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrolled_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.student.get_full_name()} enrolled in {self.course.course_code}"
    
    class Meta:
        unique_together = ['student', 'course']
        ordering = ['-enrolled_at']
        verbose_name = 'Enrollment'
        verbose_name_plural = 'Enrollments'


class AttendanceSession(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='attendance_sessions')
    session_date = models.DateField()
    session_time = models.TimeField()
    topic = models.CharField(max_length=200, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.course.course_code} - {self.session_date} {self.session_time}"
    
    def get_attendance_count(self):
        return self.attendance_records.filter(status='present').count()
    
    def get_absent_count(self):
        return self.attendance_records.filter(status='absent').count()
    
    class Meta:
        ordering = ['-session_date', '-session_time']
        unique_together = ['course', 'session_date', 'session_time']
        verbose_name = 'Attendance Session'
        verbose_name_plural = 'Attendance Sessions'


class AttendanceRecord(models.Model):
    STATUS_CHOICES = (
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
    )
    
    session = models.ForeignKey(AttendanceSession, on_delete=models.CASCADE, related_name='attendance_records')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='attendance_records', limit_choices_to={'profile__role': 'student'})
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='absent')
    remarks = models.TextField(blank=True)
    marked_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.student.get_full_name()} - {self.session.course.course_code} - {self.status}"
    
    class Meta:
        unique_together = ['session', 'student']
        ordering = ['-marked_at']
        verbose_name = 'Attendance Record'
        verbose_name_plural = 'Attendance Records'

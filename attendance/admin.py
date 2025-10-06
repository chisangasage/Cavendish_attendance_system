from django.contrib import admin
from .models import UserProfile, Course, Enrollment, AttendanceSession, AttendanceRecord

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'student_id', 'phone', 'created_at']
    list_filter = ['role', 'created_at']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'student_id']

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['course_code', 'course_name', 'lecturer', 'created_at']
    list_filter = ['created_at', 'lecturer']
    search_fields = ['course_code', 'course_name', 'description']

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'enrolled_at']
    list_filter = ['enrolled_at', 'course']
    search_fields = ['student__username', 'student__first_name', 'student__last_name', 'course__course_code']

@admin.register(AttendanceSession)
class AttendanceSessionAdmin(admin.ModelAdmin):
    list_display = ['course', 'session_date', 'session_time', 'topic', 'created_by', 'created_at']
    list_filter = ['session_date', 'course', 'created_by']
    search_fields = ['course__course_code', 'topic']

@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):
    list_display = ['student', 'session', 'status', 'marked_at']
    list_filter = ['status', 'session__session_date', 'session__course']
    search_fields = ['student__username', 'student__first_name', 'student__last_name']

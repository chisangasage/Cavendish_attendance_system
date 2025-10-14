from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', views.user_login, name='login'),
    #path('register/', views.register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    
    path('courses/', views.course_list, name='course_list'),
    path('courses/create/', views.course_create, name='course_create'),
    path('courses/<int:pk>/edit/', views.course_edit, name='course_edit'),
    path('courses/<int:pk>/delete/', views.course_delete, name='course_delete'),
    
    path('enrollments/', views.enrollment_list, name='enrollment_list'),
    path('enrollments/create/', views.enrollment_create, name='enrollment_create'),
    
    path('sessions/create/', views.attendance_session_create, name='attendance_session_create'),
    path('sessions/', views.attendance_session_list, name='attendance_session_list'),
    path('sessions/<int:session_id>/mark/', views.attendance_mark, name='attendance_mark'),
    
    path('records/', views.attendance_records, name='attendance_records'),
    path('reports/', views.reports, name='reports'),
]

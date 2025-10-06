# Attendance Management System - Cavendish University Zambia

## Project Overview
A fully functional web-based attendance management system built with Django for Cavendish University Zambia. This system automates the process of recording, tracking, and reporting student attendance, replacing the traditional manual paper-based approach.

## Purpose
The system addresses the inefficiencies of manual attendance tracking by providing:
- Automated attendance recording and tracking
- Real-time access to attendance data
- Visual analytics and comprehensive reporting
- Secure role-based access for lecturers and students
- Improved data accuracy and accessibility

## Technology Stack
- **Backend**: Django 5.2.7 (Python web framework)
- **Database**: SQLite3 (as specified in thesis)
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript
- **Charts**: Chart.js for visual attendance analytics
- **Forms**: Django Crispy Forms with Bootstrap 5 template pack

## Project Structure
```
attendance_system/          # Main Django project
├── settings.py            # Project settings and configuration
├── urls.py               # Main URL routing
└── wsgi.py               # WSGI configuration

attendance/                # Main application
├── models.py             # Database models (UserProfile, Course, Enrollment, AttendanceSession, AttendanceRecord)
├── views.py              # View functions for all features
├── forms.py              # Form definitions
├── admin.py              # Admin panel configuration
├── urls.py               # App URL routing
└── migrations/           # Database migrations

templates/                 # HTML templates
├── base.html             # Base template with navigation
└── attendance/           # App-specific templates
    ├── login.html
    ├── register.html
    ├── lecturer_dashboard.html
    ├── student_dashboard.html
    ├── course_*.html
    ├── enrollment_*.html
    ├── session_*.html
    └── reports.html

static/                    # Static files (CSS, JS)
```

## Key Features

### User Management
- **Role-based Authentication**: Separate roles for Lecturers and Students
- **User Registration**: Custom registration with role selection
- **User Profiles**: Extended user model with student IDs and contact information

### Course Management (Lecturers)
- Create, edit, and delete courses
- Assign course codes, names, and descriptions
- Track enrolled students per course

### Student Enrollment (Lecturers)
- Enroll students in courses
- View enrollment lists with filtering
- Track enrollment dates

### Attendance Management
- **Session Creation**: Create attendance sessions with date, time, and topic
- **Attendance Marking**: Mark students as Present, Absent, or Late
- **Bulk Attendance**: Mark attendance for all enrolled students at once
- **Remarks**: Add optional remarks for each attendance record

### Student Dashboard
- View all enrolled courses
- See attendance statistics per course
- Visual progress bars showing attendance rates
- Color-coded status indicators (Good/Fair/Poor)

### Lecturer Dashboard
- Overview of total courses, students, and sessions
- Quick access to recent sessions
- Course statistics at a glance

### Reports and Analytics
- **Lecturer Reports**: Generate comprehensive attendance reports by course
- **Student Analytics**: View attendance trends with interactive charts
- **Filtering**: Filter records by course, date range, and status
- **Visual Representation**: Line charts showing attendance patterns over time

## Database Models

### UserProfile
- Extends Django User model
- Fields: role (lecturer/student), student_id, phone
- One-to-one relationship with User

### Course
- Fields: course_code, course_name, description, lecturer
- Tracks enrolled students and sessions

### Enrollment
- Links students to courses
- Prevents duplicate enrollments
- Tracks enrollment dates

### AttendanceSession
- Fields: course, session_date, session_time, topic, created_by
- Represents a single class session

### AttendanceRecord
- Fields: session, student, status (present/absent/late), remarks
- Individual attendance records for each student per session

## Recent Changes
- **2025-10-06**: Initial project setup and full implementation
  - Created Django project structure
  - Implemented all database models
  - Built authentication and authorization system
  - Created all views and templates
  - Implemented attendance marking and reporting
  - Added Chart.js for visual analytics
  - Configured responsive Bootstrap UI
  - Set up workflow for development server

## User Preferences
- Time zone set to Africa/Lusaka (Zambia)
- Using Bootstrap 5 for UI consistency
- Crispy Forms for better form rendering
- Chart.js for attendance visualization

## How to Use

### First Time Setup
1. Create a superuser for admin access:
   ```bash
   python manage.py createsuperuser
   ```

2. Access the admin panel at `/admin/` to:
   - Create lecturer and student accounts
   - Set up initial courses
   - Manage system data

### Lecturer Workflow
1. Login with lecturer credentials
2. Create courses from the Courses menu
3. Enroll students in courses
4. Create attendance sessions
5. Mark attendance for each session
6. Generate reports to track student attendance

### Student Workflow
1. Login with student credentials
2. View enrolled courses
3. Check attendance records
4. View attendance trends with visual charts

## API Endpoints (URLs)
- `/` - Dashboard (redirects to role-specific dashboard)
- `/login/` - User login
- `/register/` - User registration
- `/logout/` - User logout
- `/courses/` - Course list
- `/courses/create/` - Create new course
- `/enrollments/` - Enrollment list
- `/enrollments/create/` - Enroll student
- `/sessions/` - Attendance sessions list
- `/sessions/create/` - Create new session
- `/sessions/<id>/mark/` - Mark attendance
- `/records/` - View attendance records
- `/reports/` - Generate reports

## Development Notes
- The system uses Django's built-in authentication
- SQLite database for development (can be upgraded to PostgreSQL for production)
- Responsive design works on desktop and mobile devices
- Time zone set to Africa/Lusaka (UTC+2)
- All templates extend base.html for consistent navigation and styling

## Security Features
- CSRF protection on all forms
- Login required decorators on all views
- Role-based access control
- Password validation and hashing
- Session management

## Future Enhancements (from Thesis)
- Biometric integration (fingerprint/facial recognition)
- RFID/Smart card system integration
- Mobile application (Android/iOS)
- Integration with existing university systems
- Email/SMS notifications for low attendance
- PDF/Excel export for reports
- Multi-semester and academic year management

## Deployment Considerations
- Update `SECRET_KEY` in production
- Set `DEBUG = False` in production
- Configure allowed hosts
- Use production-grade database (PostgreSQL)
- Set up static files serving with WhiteNoise or CDN
- Configure HTTPS/SSL certificates
- Set up proper backup systems

## Support and Maintenance
- Regular database backups recommended
- Monitor system performance and logs
- Update Django and dependencies regularly
- Review user feedback for improvements

---
**Project Aligned with**: Cavendish University Zambia's 8th National Development Plan and Zambia's ICT Policy (2020) for digital transformation in education.

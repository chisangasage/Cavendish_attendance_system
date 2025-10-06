# Test Credentials for CUZ Attendance System

## Admin Account
- **Username**: admin
- **Password**: admin123
- **Role**: Administrator (Lecturer)
- **Email**: admin@cuz.edu.zm

## Lecturer Account
- **Username**: hlecurer
- **Password**: lecturer123
- **Name**: Henry Sinkala
- **Email**: hsinkala@cuz.edu.zm
- **Phone**: 0977654321

## Student Accounts

### Student 1
- **Username**: hkavamba
- **Password**: student123
- **Name**: Humphrey Kavamba
- **Student ID**: CUZ2021001
- **Email**: hkavamba@cuz.edu.zm
- **Enrolled Courses**: CS301, CS302, CS303

### Student 2
- **Username**: jmwansa
- **Password**: student123
- **Name**: Jane Mwansa
- **Student ID**: CUZ2021002
- **Email**: jmwansa@cuz.edu.zm
- **Enrolled Courses**: CS301, CS302

### Student 3
- **Username**: pchanda
- **Password**: student123
- **Name**: Peter Chanda
- **Student ID**: CUZ2021003
- **Email**: pchanda@cuz.edu.zm
- **Enrolled Courses**: CS301, CS303

## Sample Courses

### CS301 - Web Development
- **Description**: Introduction to modern web development using Django and React
- **Lecturer**: Henry Sinkala
- **Enrolled Students**: 3

### CS302 - Database Systems
- **Description**: Design and implementation of relational database systems
- **Lecturer**: Henry Sinkala
- **Enrolled Students**: 2

### CS303 - Software Engineering
- **Description**: Software development methodologies and best practices
- **Lecturer**: Henry Sinkala
- **Enrolled Students**: 2

## Test Data Summary
- **Total Lecturers**: 2 (including admin)
- **Total Students**: 3
- **Total Courses**: 3
- **Total Enrollments**: 7
- **Total Sessions**: 5
- **Total Attendance Records**: 13

## How to Test

1. **Login as Lecturer** (hlecurer/lecturer123)
   - View lecturer dashboard with course statistics
   - Create new courses
   - Enroll students
   - Create attendance sessions
   - Mark attendance
   - Generate reports

2. **Login as Student** (hkavamba/student123)
   - View student dashboard with attendance overview
   - Check enrolled courses
   - View attendance records with visual charts
   - Track attendance trends

3. **Admin Panel** (/admin/)
   - Login with admin/admin123
   - Manage all users, courses, and attendance data
   - Access full administrative features

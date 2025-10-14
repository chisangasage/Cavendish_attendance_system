Cavendish University Zambia — Attendance Management Web Application
📘 Overview

This project is a Web-Based Course Attendance Management System designed for Cavendish University Zambia (CUZ).
It allows lecturers to manage courses and record student attendance efficiently, while students can view attendance records, course details, and performance analytics.

The system includes:

Secure authentication for both lecturers and students
Role-based dashboards
Attendance marking & tracking
Course and enrolment management
MySQL database integration

⚙️ Installation & Setup Guide
1️⃣ Clone or Extract the Project

If you’ve received a .zip file, extract it and navigate to the project root directory (where manage.py is located):

cd CUZATTENDANCE

2️⃣ Create a Virtual Environment

Create and activate a virtual environment to isolate dependencies:

python3 -m venv myenv
source myenv/bin/activate   # For Linux/Mac
myenv\Scripts\activate      # For Windows

3️⃣ Install Required Packages

Use the provided requirements.txt to install dependencies:

pip install -r requirements.txt

4️⃣  Apply Migrations

Once the database is configured, run:

python manage.py makemigrations
python manage.py migrate

5️⃣ Run the Development Server

Start the Django server:

python manage.py runserver


Now visit:

http://127.0.0.1:8000/

🔑 Login Credentials (for testing)

Sample test credentials are stored in the file:

TEST_CREDENTIALS.txt


This file includes student and lecturer demo accounts that you can use to explore system functionality.

🧱 Core Features
User Type	Capabilities
Lecturer	Add students to courses, mark attendance, view attendance reports
Student	View personal attendance dashboard, course list, and analytics
Admin	Manage users, courses, and sessions via Django Admin interface
🧰 Tech Stack

Frontend: HTML5, CSS3, JavaScript (Bootstrap UI)

Backend: Django 5.x (Python 3.12)

Database: SQLite

Environment: Ubuntu/Linux (recommended)

🧪 Testing

Use the provided credentials in TEST_CREDENTIALS.txt to simulate real interactions:

Login as a lecturer to manage courses and attendance

Login as a student to view attendance analytics

👨‍💻 Developed By

Chisanga Kabwe
Bachelor of Science in computing
School of Business and Information Technology, Cavendish University Zambia

📅 Project Timeline
Phase	Duration	Status
Project Setup & Environment	1 week	✅ Complete
Backend Development	        2 weeks	✅ Complete
Frontend & UI Integration	1 week	✅ Complete
Testing & Deployment	    1 week	✅ Complete
🪪 License

This project is developed for academic purposes under the supervision of Cavendish University Zambia.
Unauthorized commercial use is not permitted.

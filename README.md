# SkillLearner

SkillLearner is a Django-based mentorship booking platform where students can discover teachers, send mentorship booking requests, and track their booking status. Teachers can manage their profiles and approve or reject booking requests.

This project demonstrates role-based authentication, REST APIs, and a booking workflow system built using Django and Django REST Framework.

---

## Features

### Authentication

* User signup with role selection (Teacher / Student)
* Secure login and logout system
* Role-based access control

### Teacher Features

* Create and edit teacher profile
* Add skills, experience, availability, and charges
* View incoming booking requests
* Approve or reject booking requests

### Student Features

* Browse available teachers
* Send booking requests
* Track booking status (Pending / Approved / Rejected)
* Cancel pending booking requests

### Booking System

* Prevents duplicate bookings
* Tracks booking status
* Teacher decision updates student dashboard

---

## Tech Stack

### Backend

* Python
* Django
* Django REST Framework

### Frontend

* HTML
* CSS
* JavaScript

### Database

* SQLite (development)

---

## Project Structure

skill-learner
│
├── skillswap
│   ├── skills
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── templates
│   │
│   ├── skillswap
│   │   └── settings.py
│   │
│   └── manage.py
│
├── requirements.txt
├── .gitignore
└── README.md

---

## API Endpoints

### Authentication

Signup
POST /api/signup/

Login
POST /api/login/

---

### Teachers

Get teacher list
GET /api/teachers/

Edit teacher profile
PUT /api/teacher/profile/

---

### Bookings

Create booking request
POST /api/book/

Teacher view bookings
GET /api/teacher/bookings/

Teacher update booking status
PUT /api/teacher/bookings/{id}/

Student view bookings
GET /api/student/bookings/

Student cancel booking
DELETE /api/student/bookings/{id}/

---

## How to Run the Project

Clone the repository

git clone https://github.com/Raunaksharma0410/skill-learner.git

Go to project folder

cd skill-learner

Install dependencies

pip install -r requirements.txt

Run migrations

python manage.py migrate

Start server

python manage.py runserver

Open in browser

http://127.0.0.1:8000

---

## Key Concepts Demonstrated

* Role-based authentication
* REST API design using Django REST Framework
* Booking workflow implementation
* Serializer-based data validation
* Permission-based API access
* Django template integration with APIs

---

## Author

Ronak Sharma
Aspiring Django Backend Developer

GitHub
https://github.com/Raunaksharma0410

---

## Future Improvements

* Payment integration
* Email notifications for booking updates
* Teacher profile image upload
* Deployment on cloud (AWS / Render)

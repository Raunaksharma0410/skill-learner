from django.urls import path, include
from .views import (
    signup_view,
    teacher_profile_view,
    teacher_list_view,
    create_booking_view,
    teacher_bookings_view,
    update_booking_status_view,
    student_bookings_view,
    teacher_dashboard_view,
    home_page,
    signup_page,
    login_page,
    logout_view,
    teachers_page,
    teacher_profile_page,
    teacher_bookings_page,
    student_bookings_page,
    delete_student_booking_view
)

urlpatterns = [

    # 🔹 Frontend Pages
    path('', home_page, name='home'),
    path('signup/', signup_page, name='signup'),
    path('login/', login_page, name='login'),
    path('logout/', logout_view, name='logout'),
    path('teachers-page/', teachers_page, name='teachers-page'),
    path('teacher/profile/edit/', teacher_profile_page, name='teacher-profile-page'),
    path('teacher/bookings/', teacher_bookings_page, name='teacher-bookings-page'),


    # 🔹 API Endpoints (NO MORE CONFLICTS)
    path('api/signup/', signup_view, name='api-signup'),
    path('api/teacher/profile/', teacher_profile_view, name='api-teacher-profile'),
    path('api/teachers/', teacher_list_view, name='api-teacher-list'),
    path('student/bookings/', student_bookings_page, name='student-bookings-page'),
    path('api/book/', create_booking_view, name='api-create-booking'),
    path('api/teacher/bookings/', teacher_bookings_view, name='api-teacher-bookings'),
    path('api/teacher/bookings/<int:booking_id>/', update_booking_status_view, name='api-update-booking'),
    path('api/student/bookings/', student_bookings_view, name='api-student-bookings'),
    path('api/teacher/dashboard/', teacher_dashboard_view, name='api-teacher-dashboard'),
    path('api/student/bookings/<int:booking_id>/', delete_student_booking_view, name='delete-student-booking'),
]
# Django
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import logout, authenticate, login
from django.db.models import Count

# DRF
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

# Local app
from .models import Booking, UserProfile, Student_profile, Teacher_profile
from .serializers import SignupSerializer, BookingSerializer, TeacherProfileSerializer



# =========================================================
# FRONTEND PAGE VIEWS
# =========================================================

def home_page(request):
    return render(request, 'homepage.html')


def teachers_page(request):
    return render(request, 'teacher.html')


def teacher_profile_page(request):
    if not request.user.is_authenticated:
        return redirect("login")

    if request.user.userprofile.role != "teacher":
        return redirect("home")

    return render(request, "teacher_profile_edit.html")


def teacher_bookings_page(request):
    if not request.user.is_authenticated:
        return redirect("login")

    if request.user.userprofile.role != "teacher":
        return redirect("home")

    return render(request, "teacher_booking.html")


def student_bookings_page(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.user.userprofile.role != "student":
        return redirect('home')

    return render(request, "student_booking.html")


# =========================================================
# AUTHENTICATION (FRONTEND)
# =========================================================

def signup_page(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        role = request.POST.get("role")

        if User.objects.filter(username=username).exists():
            return render(request, "signup.html", {"error": "Username already exists"})

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        UserProfile.objects.create(user=user, role=role)

        if role == "teacher":
            Teacher_profile.objects.create(user=user)
        else:
            Student_profile.objects.create(user=user)

        login(request, user)
        return redirect("home")

    return render(request, "signup.html")


def login_page(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            return render(request, "login.html", {"error": "Invalid credentials"})

    return render(request, "login.html")


def logout_view(request):
    logout(request)
    return redirect("home")


# =========================================================
# AUTHENTICATION API
# =========================================================

@api_view(['POST'])
@permission_classes([AllowAny])
def signup_view(request):
    serializer = SignupSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response({"message": "User created successfully"}, status=201)

    return Response(serializer.errors, status=400)


# =========================================================
# TEACHER PROFILE API
# =========================================================

@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def teacher_profile_view(request):

    if request.user.userprofile.role != 'teacher':
        return Response(
            {"error": "Only teachers can access this endpoint"},
            status=status.HTTP_403_FORBIDDEN
        )

    teacher_profile = Teacher_profile.objects.get(user=request.user)

    if request.method == 'GET':
        serializer = TeacherProfileSerializer(teacher_profile)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = TeacherProfileSerializer(
            teacher_profile,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)


# =========================================================
# TEACHER LIST API (STUDENT SIDE)
# =========================================================

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def teacher_list_view(request):

    if request.user.userprofile.role != 'student':
        return Response({"error": "Only students can view teachers"}, status=403)

    teachers = Teacher_profile.objects.all()
    result = []

    for teacher in teachers:
        booking = Booking.objects.filter(
            teacher=teacher.user,
            student=request.user
        ).first()

        result.append({
            "id": teacher.user.id,
            "username": teacher.user.username,
            "teacher_skill": teacher.teacher_skill,
            "teacher_experience": teacher.teacher_experience,
            "teacher_charge": teacher.teacher_charge,
            "teacher_availability": teacher.teacher_availability,
            "booking_status": booking.status if booking else None
        })

    return Response(result)


# =========================================================
# BOOKING APIs
# =========================================================

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_booking_view(request):

    if request.user.userprofile.role != 'student':
        return Response(
            {"error": "Only students can create bookings"},
            status=status.HTTP_403_FORBIDDEN
        )

    teacher_id = request.data.get('teacher')

    try:
        teacher = User.objects.get(id=teacher_id)
    except User.DoesNotExist:
        return Response({"error": "Teacher not found"}, status=404)

    serializer = BookingSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save(student=request.user, teacher=teacher)
        return Response(serializer.data, status=201)

    return Response(serializer.errors, status=400)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def teacher_bookings_view(request):

    if request.user.userprofile.role != 'teacher':
        return Response(
            {"error": "Only teachers can view bookings"},
            status=status.HTTP_403_FORBIDDEN
        )

    bookings = Booking.objects.filter(teacher=request.user)
    serializer = BookingSerializer(bookings, many=True)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_booking_status_view(request, booking_id):

    if request.user.userprofile.role != 'teacher':
        return Response(
            {"error": "Only teachers can update booking status"},
            status=status.HTTP_403_FORBIDDEN
        )

    try:
        booking = Booking.objects.get(id=booking_id, teacher=request.user)
    except Booking.DoesNotExist:
        return Response({"error": "Booking not found"}, status=404)

    new_status = request.data.get('status')

    if new_status not in ['approved', 'rejected']:
        return Response({"error": "Status must be approved or rejected"}, status=400)

    booking.status = new_status
    booking.save()

    serializer = BookingSerializer(booking)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def student_bookings_view(request):

    if request.user.userprofile.role != 'student':
        return Response(
            {"error": "Only students can view their bookings"},
            status=403
        )

    bookings = Booking.objects.filter(student=request.user)
    serializer = BookingSerializer(bookings, many=True)
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_student_booking_view(request, booking_id):

    if request.user.userprofile.role != "student":
        return Response({"error": "Only students can cancel"}, status=403)

    try:
        booking = Booking.objects.get(id=booking_id, student=request.user)
    except Booking.DoesNotExist:
        return Response({"error": "Booking not found"}, status=404)

    if booking.status != "pending":
        return Response({"error": "Cannot cancel after approval"}, status=400)

    booking.delete()
    return Response({"message": "Booking cancelled"}, status=200)


# =========================================================
# DASHBOARD API
# =========================================================

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def teacher_dashboard_view(request):

    if request.user.userprofile.role != 'teacher':
        return Response({"error": "Only teachers can access dashboard"}, status=403)

    bookings = Booking.objects.filter(teacher=request.user)

    data = {
        "total_bookings": bookings.count(),
        "pending": bookings.filter(status='pending').count(),
        "approved": bookings.filter(status='approved').count(),
        "rejected": bookings.filter(status='rejected').count(),
    }

    return Response(data)
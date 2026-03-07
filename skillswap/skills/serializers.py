# =========================================================
# DJANGO & DRF IMPORTS
# =========================================================

from rest_framework import serializers
from django.contrib.auth.models import User

# Local app models
from .models import UserProfile, Teacher_profile, Student_profile, Booking


# =========================================================
# AUTHENTICATION SERIALIZERS
# =========================================================

class SignupSerializer(serializers.ModelSerializer):
    """
    Handles user registration with role-based profile creation.
    Creates:
    - User
    - UserProfile
    - Teacher_profile or Student_profile
    """

    role = serializers.ChoiceField(choices=UserProfile.ROLE_CHOICES)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):

        # Extract role & password
        role = validated_data.pop('role')
        password = validated_data.pop('password')

        # Create base user
        user = User(**validated_data)
        user.set_password(password)
        user.save()

        # Create role profile
        UserProfile.objects.create(user=user, role=role)

        # Create specific profile based on role
        if role == 'teacher':
            Teacher_profile.objects.create(user=user)
        else:
            Student_profile.objects.create(user=user)

        return user


# =========================================================
# TEACHER SERIALIZER
# =========================================================

class TeacherProfileSerializer(serializers.ModelSerializer):
    """
    Serializes teacher profile along with user information.
    """

    id = serializers.IntegerField(source='user.id', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = Teacher_profile
        fields = [
            'id',
            'username',
            'email',
            'teacher_phone',
            'teacher_experience',
            'teacher_skill',
            'teacher_charge',
            'teacher_availability'
        ]


# =========================================================
# BOOKING SERIALIZER
# =========================================================

class BookingSerializer(serializers.ModelSerializer):
    """
    Serializes booking information.
    Includes:
    - Student username
    - Teacher username
    - Teacher skill & charge (via Teacher_profile)
    """

    student = serializers.CharField(source='student.username', read_only=True)
    teacher_name = serializers.CharField(source='teacher.username', read_only=True)

    # Fetch data from related Teacher_profile model
    teacher_skill = serializers.CharField(
        source='teacher.teacher_profile.teacher_skill',
        read_only=True
    )

    teacher_charge = serializers.IntegerField(
        source='teacher.teacher_profile.teacher_charge',
        read_only=True
    )

    class Meta:
        model = Booking
        fields = [
            'id',
            'student',
            'teacher',
            'teacher_name',
            'teacher_skill',
            'teacher_charge',
            'date',
            'time',
            'status'
        ]
        read_only_fields = ['status']
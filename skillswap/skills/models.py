from django.db import models
from django.contrib.auth.models import User

#User profile
class UserProfile(models.Model):

    ROLE_CHOICES = (
        ('teacher', 'Teacher'),
        ('student', 'Student'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.user.username} - {self.role}"

#Teacher profile
class Teacher_profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    teacher_phone = models.CharField(max_length=20, blank=True, null=True)
    teacher_experience = models.IntegerField(blank=True, null=True)
    teacher_skill = models.CharField(max_length=100, blank=True, null=True)
    teacher_charge = models.IntegerField(blank=True, null=True)
    teacher_availability = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - Teacher Profile"

#student profile

class Student_profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Student: {self.user.username}"

#Booking
class Booking(models.Model):

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )

    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='student_bookings')
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='teacher_bookings')

    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    # 🔥 ADD THIS PART
    class Meta:
        unique_together = ('student', 'teacher')

    def __str__(self):
        return f"{self.student.username} → {self.teacher.username} ({self.status})"
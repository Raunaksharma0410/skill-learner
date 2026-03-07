
from django.contrib import admin
from .models import UserProfile, Teacher_profile, Student_profile, Booking

admin.site.register(UserProfile)
admin.site.register(Teacher_profile)
admin.site.register(Student_profile)
admin.site.register(Booking)



# Register your models here.

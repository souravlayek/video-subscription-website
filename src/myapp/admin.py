from django.contrib import admin
from .models import Course, Lesson, CourseRequested, Profile
# Register your models here.
admin.site.register(Course)
admin.site.register(Lesson)
admin.site.register(CourseRequested)
admin.site.register(Profile)




from django.urls import path

from .views import index, AddCourse, courseDetail, addLesson, viewLesson, courseList, requestCourse, requestList, acceptRequest,Profile
urlpatterns = [
    path('', index, name="home"),
    path('course/<slug:slug>', courseDetail, name="course"),
    path('addCourse', AddCourse.as_view(), name="addCourse"),
    path('addlesson/<slug:slug>',addLesson, name="addLesson"),
    path('addlesson/<slug:slug>',addLesson, name="addLesson"),
    path('<course_slug>/lesson/<slug:slug>',viewLesson, name="lesson"),
    path("mycourses", courseList, name="courseList"),
    path("requestCourse/<slug:slug>", requestCourse, name="requestCourse"),
    path("requestList/", requestList, name="requestList"),
    path("acceptRequest/<id>", acceptRequest, name="acceptRequest"),
    path("profile/", Profile.as_view(), name="profile"),

]
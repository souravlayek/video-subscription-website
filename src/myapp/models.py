from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from elearning.utils import unique_slug_generator
from django.urls import reverse
# slug = models.SlugField(max_length=250, blank=True, null=True)

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField()
    description = models.CharField(max_length=250)
    updated =models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

class Lesson(models.Model):
    slug = models.SlugField(max_length=250, blank=True, null=True)
    course = models.ForeignKey("Course",related_name="lessons", on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    thumbnail = models.ImageField(upload_to="thumbnail/" ,null=True)
    video_url = models.URLField(max_length=200)
    description = models.CharField(max_length=250)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("lesson", kwargs={"course_slug":self.course.slug ,"slug": self.slug})
    


class Course(models.Model):
    slug = models.SlugField(max_length=250, blank=True, null=True)
    author = models.ForeignKey(User,related_name = "author", on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=250)
    students = models.ManyToManyField(User,related_name = "student", blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("course", kwargs={"slug": self.slug})

    @property
    def get_lesson(self):
        return self.lessons.all()



class CourseRequested(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    requested_user = models.ForeignKey(User, on_delete=models.CASCADE)
    approved = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.course.name


def slug_generator(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(slug_generator, sender=Course)
pre_save.connect(slug_generator, sender=Lesson)



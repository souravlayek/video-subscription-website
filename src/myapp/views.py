from django.shortcuts import render,redirect, get_object_or_404, reverse
from .models import Course,Lesson, CourseRequested
from .forms import AddCourseForm,AddLessonForm
from django.views import View
from django.views.generic import DetailView,CreateView
from django.contrib import messages
from django.views.generic.base import TemplateView

def index(request):
    courses = Course.objects.all()
    context = {
        "courses": courses
    }
    return render(request, "index.html", context)


class AddCourse(View):
    form_class = AddCourseForm
    template_name = "add_course.html"

    def get(self, request, *args, **kwargs):
        context = {
        "form": self.form_class()
        }
        return render(request, self.template_name, context)
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            myCourse = Course()
            myCourse.name = form.cleaned_data['name']
            myCourse.description = form.cleaned_data['description']
            myCourse.author = request.user
            myCourse.save()
            messages.success(request, "added successfully")
            return redirect('home')
        messages.warning(request, "enter a valid details")
    
        return redirect('addCourse')
    

def courseDetail(request, slug):
    course = get_object_or_404(Course, slug=slug)
    permited = False
    students = course.students.filter(username = request.user.username)
    print(students)
    for i in students:
        if i.id == request.user.id:
            permited = True
            break
    if course.author.id == request.user.id:
        permited=True
    return render(request, "course.html", {"course": course,"permited":permited })
        

def addLesson(request, slug):
    if request.method == "POST":
        form = AddLessonForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                instances = form.save(commit=False)
                course = get_object_or_404(Course,slug=slug)
                instances.course = course
                instances.save()
                messages.success(request, "added successfully")
                return redirect(reverse("course", kwargs={"slug": slug}))
            except:
                messages.success(request, "added successfully")
                return redirect(reverse("course", kwargs={"slug": slug}))
        else:
            messages.warning(request, "invalid details")
            return reverse("addLesson", kwargs={"slug": slug})
    else:
        form = AddLessonForm
        return render(request, "addlesson.html", {"form": form})

def viewLesson(request, slug, course_slug):
    lesson = get_object_or_404(Lesson,slug=slug)
    course = lesson.course
    permited = False
    if request.user in course.students.all():
        permited=True
    if request.user.id == course.author.id:
        permited = True
    context = {
        "permited": permited,
        "lesson": lesson
    }
    return render(request, "view_lesson.html",context)

def courseList(request):
    courses = Course.objects.filter(author=request.user)
    return render(request, "courselist.html", {"courses":courses})

def requestCourse(request, slug):
    courses =get_object_or_404(Course, slug=slug)
    qs = CourseRequested()
    qs.course = courses
    qs.requested_user = request.user
    qs.save()
    return redirect('course',slug)

def requestList(request):
    qs = CourseRequested.objects.all()
    l1 = []
    for i in qs:
        if i.course.author.id == request.user.id:
            if not i.approved:
                l1.append(i)
    return render(request,"requestlist.html", {"qs":l1})

def acceptRequest(request, id):
    qs = get_object_or_404(CourseRequested, id=id)
    qs.approved = True
    qs.save()
    course = qs.course
    course.students.add(qs.requested_user)
    course.save()
    return redirect("requestList")


class Profile(TemplateView):
    template_name = 'profile.html'
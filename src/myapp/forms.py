from django.contrib.auth import get_user_model
from django import forms
from .models import Course, Lesson

class SignupForm(forms.ModelForm):
    teacher_or_not = forms.BooleanField(required=False, label="I am a Teacher")
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name']

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if self.cleaned_data["teacher_or_not"]:
            user.is_staff = True
        user.save()

class AddCourseForm(forms.ModelForm):
    class Meta:
        model = Course
        widgets = {"description": forms.Textarea(attrs={'cols': 5, 'rows': 5})}
        fields = ["name","description"]

class AddLessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        widgets = {"description": forms.Textarea(attrs={'cols': 5, 'rows': 5})}
        fields = ["name","description","thumbnail" ,"video_url"]

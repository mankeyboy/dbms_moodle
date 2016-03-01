from django import forms

from .models import *

class StudentSignUpForm(forms.ModelForm):
	class Meta:
		model = Student
		fields = ['name','email','password','phone','address','dob','year','department','institute','parent_email_id']

class FacultySignUpForm(forms.ModelForm):
	class Meta:
		model = Faculty
		fields = ['name','email','password','phone','address','dob','department','institute']

class StudentLogInForm(forms.ModelForm):
	class Meta:
		model = Student
		fields = ['email','password']

class RegisterCourseForm(forms.ModelForm):
	class Meta:
		model = Course
		fields = ['name','credits','durationWeeks','fees']
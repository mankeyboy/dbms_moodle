from django import forms
from django.forms.models import inlineformset_factory, modelformset_factory
from django.forms.formsets import BaseFormSet

from .models import *

class StudentSignUpForm(forms.ModelForm):
	class Meta:
		model = Student
		fields = ['name','email','password','phone','address','dob','year','department','institute','parent_email_id']

class FacultySignUpForm(forms.ModelForm):
	class Meta:
		model = PendingFaculty
		fields = ['name','email','password','phone','address','dob','department','institute']

class StudentLogInForm(forms.ModelForm):
	class Meta:
		model = Student
		fields = ['email','password']

class RegisterCourseForm(forms.ModelForm):
	class Meta:
		model = Course
		fields = ['name','credits','durationWeeks','fees']

class CalendarForm(forms.ModelForm):
	class Meta:
		model = Calendar
		fields = ['date','content','quiz']

class MailForm(forms.ModelForm):
	class Meta:
		model = Notif
		fields = ['notif_to_role','notif_to_id','text']

class ParentSignInForm(forms.ModelForm):
	class Meta:
		model=Student
		fields=['email','dob']


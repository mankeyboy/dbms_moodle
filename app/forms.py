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

class CalendarForm(forms.ModelForm):
	class Meta:
		model = Calendar
		fields = ['date','content']
		exclude = None

class QuestionForm(forms.ModelForm):
	class Meta:
		model = Question
		fields = ['text','op1','op2','op3','op4','answer']
		exclude = None

class BaseQuestionFormSet(BaseFormSet):
	pass
# QuestionFormSet = modelformset_factory(Question,fields=None,exclude=None)
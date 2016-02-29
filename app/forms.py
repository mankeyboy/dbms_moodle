from django import forms

from .models import Student

class StudentSignUpForm(forms.ModelForm):
	class Meta:
		model = Student
		fields = ['name','email','password','phone','address','dob','year','department','institute','parent_email_id']

class StudentLogInForm(forms.ModelForm):
	class Meta:
		model = Student
		fields = ['email','password']
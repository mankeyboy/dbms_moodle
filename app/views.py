from django.shortcuts import render, render_to_response	, HttpResponse
from forms import StudentSignUpForm
from models import Student
# Create your views here.
def gaaliDe(request):
	if request.method=='POST':
		form = StudentSignUpForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponse("Congrats! You have been registered on Coursera")
		else:
			return HttpResponse("Email Id or Phone no. has been already Registered (Validation Failed)")
		# context = {
		# "title":"Congrats! You have been registered on Coursera",
		# "form": form,
		# }
		
	else:
		form = StudentSignUpForm()
		context = {
		"title":"Register On Coursera",
		"form": form,
		}
		return render(request,"app/studentSignUp.html",context)
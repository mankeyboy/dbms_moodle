from django.shortcuts import render, render_to_response , HttpResponse
from forms import StudentSignUpForm, StudentLogInForm
from models import Student
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.
def studentSignUp(request):
    if request.method=='POST':
        form = StudentSignUpForm(request.POST)
        print form
        if form.is_valid():
            user = User.objects.create_user(form.cleaned_data.get('email'),form.cleaned_data.get('email'),form.cleaned_data.get('password'))
            form.save()
            roll = Student.objects.get(email=form.cleaned_data.get('email'))
            print type(roll.ID)
            print roll.ID
            return HttpResponse("Congrats! You have been registered on Coursera.\n Your roll no is "+str(roll.ID))
        else:
            return HttpResponse("Email Id or Phone no. has been already Registered (Validation Failed)")
        # context = {
        # "title":"Congrats! You have been registered on Coursera",
        # "form": form,
        # }
        
    else:
        form = StudentSignUpForm()
        print "Coming there"
        context = {
        "title":"Register On Coursera",
        "form": form,
        }
        return render(request,"app/studentSignUp.html",context)

# def showRoll(request):
#   roll_info = Student.objects.get()
#   print roll_info
#   context = RequestContext(request)
#   return render_to_response('app/confirmation.html',data,context)
def studentLogIn(request):
    if request.method=='POST':
        form = StudentLogInForm(request.POST)
        print form
        user = authenticate(username=form.cleaned_data.get('email'), password=form.cleaned_data.get('password'))
        print form.cleaned_data.get('email')
        print form.cleaned_data.get('password')
        if user is not None:
            # the password verified for the user
            if user.is_active:
                print("User is valid, active and authenticated")
            else:
                print("The password is valid, but the account has been disabled!")
        else:
            # the authentication system was unable to verify the username and password
            print("The username and password were incorrect.")
        return HttpResponse("Machaaya")
    else:
        form = StudentLogInForm()
        print "Coming here"
        context = {
        "form": form,
        }
        return render(request,"app/studentSignUp.html",context)

def loginStudent(request):
    logout(request)
    username = password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                # return HttpResponseRedirect('/main/')
                context={
                "username" : username
                }
                return HttpResponseRedirect('/studenthome/')
    return render_to_response('app/login.html', context_instance=RequestContext(request))

def logout_view(request):
    logout(request)
    # Redirect to a success page.

@login_required(login_url='/login/')
def studenthome(request):
    return render_to_response('app/studenthome.html', context_instance=RequestContext(request))
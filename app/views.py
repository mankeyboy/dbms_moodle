from django.shortcuts import render, render_to_response , HttpResponse
from forms import *
from models import *
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test

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
        "who" : "Student",
        "title":"Register On Coursera",
        "form": form,
        }
        return render(request,"app/studentSignUp.html",context)

def facultySignUp(request):
    if request.method=='POST':
        form = FacultySignUpForm(request.POST)
        print form
        if form.is_valid():
            user = User.objects.create_user(form.cleaned_data.get('email'),form.cleaned_data.get('email'),form.cleaned_data.get('password'))
            form.save()
            roll = Faculty.objects.get(email=form.cleaned_data.get('email'))
            print type(roll.ID)
            print roll.ID
            return HttpResponse("Congrats! You have been registered on Coursera as a faculty.\n Your faculty ID is "+str(roll.ID))
        else:
            return HttpResponse("Email Id or Phone no. has been already Registered (Validation Failed)")
        # context = {
        # "title":"Congrats! You have been registered on Coursera",
        # "form": form,
        # }
        
    else:
        form = FacultySignUpForm()
        print "Coming there"
        context = {
        "who" : "Faculty",
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
                try:
                    TheStudent = Student.objects.get(email=username)
                    if TheStudent is not None:
                        context={
                        "username" : username
                        }
                        return HttpResponseRedirect('/studenthome/')
                except:
                    try:
                        TheFaculty = Faculty.objects.get(email=username)
                        if TheFaculty is not None:
                            return HttpResponseRedirect('/facultyhome')
                    except:
                        TheAdmin = Admin.objects.get(email = username)
                        if TheAdmin is not None:
                            return HttpResponseRedirect('/adminhome')
                        else:
                            return HttpResponse("What the hell!!! -_-")

        else:
            return HttpResponseRedirect('/login')
    return render_to_response('app/login.html', context_instance=RequestContext(request))

def logout_view(request):
    logout(request)
    # Redirect to a success page.

@login_required(login_url='/login/')
def studenthome(request):
    if request.method == 'POST':
        registered_courses = Course.objects.filter(student__email = 'xyz')
        courses_offered = Course.objects.all()
        course_info = Calendar.objects.raw('Select * from Calendar where Calendar.course_id in ( select course_id from registered_courses) and Calender.date > datetime.now()')
        course_data = {
               "course_list" : registered_courses,
               "course_offered_list" : courses_offered,
                "course_calendars"    : course_info,
        }
    
    return render_to_response('app/home.html', context_instance=RequestContext(request))


def isFaculty(user):
    try:
        fac = Faculty.objects.get(email=user.username)
        if fac is not None:
            return True
        return False
    except:
        return False


@user_passes_test(isFaculty,login_url = '/login/faculty')
def offerCourse(request):
    if request.method=='POST':
        form = RegisterCourseForm(request.POST)
        print form
        if form.is_valid():
            obj = form.save(commit=False)
            print request.user.username
            fac = Faculty.objects.get(email = request.user.username)
            print fac
            obj.save()
            obj.faculty.add(fac)
            obj.save()

            return HttpResponse("The Course has been registered on Coursera.\n The course ID is "+str('roll.ID - Abhi peace maar :P'))
        else:
            return HttpResponse("Course Validation Failed")
        # context = {
        # "title":"Congrats! You have been registered on Coursera",
        # "form": form,
        # }
        
    else:
        form = RegisterCourseForm()
        print "Coming there"
        context = {
        "who" : "Course",
        "title":"Register Course",
        "form": form,
        }
        return render(request,"app/studentSignUp.html",context)







# def HomeStudent(request):
#     if request.method == 'POST'
        
#         registered_courses = Course.objects.filter(student__email = 'xyz')
#         courses_offered = Course.objects.all()
#         for course_info in Calendar.objects.raw(Select * from Calendar where 
#                                                 Calendar.course_id in ( select course_id from registered_courses)
#                                                 and Calender.date >datetime.now())
#         course_data = {
#                "course_list" : registered_courses
#                "course_offered_list" : courses_offered
#                 "course_calendars"    : course_info
#         }
        
#         return render_to_response("app/home.html",course_data,context_instance=RequestContext(request))

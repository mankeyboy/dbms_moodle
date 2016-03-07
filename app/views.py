from django.shortcuts import render, render_to_response , HttpResponse
from forms import *
from models import *
from django.contrib import messages
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.generic import CreateView
from django.forms.formsets import formset_factory
# from django.core.urlresolvers import resolve



# Create your views here.



def home(request):
    print request.user.username
    courses_offered = Course.objects.all()
    course_info = Calendar.objects.filter(course=courses_offered)
    course_data = {
            "name" : request.user.username,
            "course_offered_list" : courses_offered,
            "course_calendars"    : course_info,
    }

    return render_to_response('app/home.html',course_data)



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
        
    else:
        form = StudentSignUpForm()
        print form
        print "Coming there"
        context = {
        "who" : "Student",
        "title":"Register On Coursera",
        "form": form,
        }
        print render(request,"app/studentSignUp.html",context)
        return render(request,"app/studentSignUp.html",context)

def sendmail(request):
    print "YO"
    if request.method=='POST':
        form = MailForm(request.POST)
        print form
        print "yo"
        if form.is_valid():
            mail=form.save(commit=False)
            username=request.user.username
            #   TheStudent = Student.objects.get(email=username)
            try:
                TheStudent = Student.objects.get(email=username)
                if TheStudent is not None:
                    mail.notif_from_role='S'
                    mail.notif_from_id=TheStudent.ID
                    mail.save()
                    
            except:
                TheFaculty = Faculty.objects.get(email=username)
                if TheFaculty is not None:
                    mail.notif_from_role='F'
                    mail.notif_from_id=TheFaculty.ID
                    mail.save()

            return HttpResponse("mail sent")
        else:
            return HttpResponse("mail not sent .try again")
    else:
        form = MailForm()
        context={
        "form" :form,
        }
        return render(request,"app/sendmail.html",context)

def facultySignUp(request):
    if request.method=='POST':
        form = FacultySignUpForm(request.POST)
        print form
        if form.is_valid():
            user = User.objects.create_user(form.cleaned_data.get('email'),form.cleaned_data.get('email'),form.cleaned_data.get('password'))
            form.save()
            return HttpResponse("Your request has been sent" )
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


# def studentLogIn(request):
#     if request.method=='POST':
#         form = StudentLogInForm(request.POST)
#         print form
#         user = authenticate(username=form.cleaned_data.get('email'), password=form.cleaned_data.get('password'))
#         print form.cleaned_data.get('email')
#         print form.cleaned_data.get('password')
#         if user is not None:
#             # the password verified for the user
#             if user.is_active:
#                 print("User is valid, active and authenticated")
#             else:
#                 print("The password is valid, but the account has been disabled!")
#         else:
#             # the authentication system was unable to verify the username and password
#             print("The username and password were incorrect.")
#         return HttpResponse("Machaaya")
#     else:
#         form = StudentLogInForm()
#         print "Coming here"
#         context = {
#         "form": form,
#         }
#         return render(request,"app/studentSignUp.html",context)

def login_user(request):
    # user2 = User.objects.create_user('admin@gmail.com','admin@gmail.com','admin')
    logout(request)
    username = password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        print user
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
    return HttpResponseRedirect('/')
    # Redirect to a success page.

def isStudent(user):
    try:
        stud = Student.objects.get(email=user.username)
        if stud is not None:
            return True
        return False
    except:
        return False


def isFaculty(user):
    try:
        fac = Faculty.objects.get(email=user.username)
        if fac is not None:
            return True
        return False
    except:
        return False


@user_passes_test(isFaculty,login_url = '/login/faculty/')
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
        
    else:
        form = RegisterCourseForm()
        print "Coming there"
        context = {
        "who" : "Course",
        "title":"Register Course",
        "form": form,
        }
        return render(request,"app/studentSignUp.html",context)


@user_passes_test(isStudent,login_url = '/login/student/')
def studenthome(request):
    print request.user.username
    students= Student.objects.get(email=request.user.username)
    registered_courses = Course.objects.filter(student=students)
    courses_offered = Course.objects.all()
    course_info = Calendar.objects.filter(course=registered_courses)
    mails=Notif.objects.filter(notif_to_id=students.ID).filter(notif_to_role='S')
    print students.ID
    course_data = {
            "name" : request.user.username,
           "course_list" : registered_courses,
           "course_offered_list" : courses_offered,
            "course_calendars"    : course_info,
            "mail" : mails,
    }
    return render_to_response('app/studenthome.html',course_data)

def adminhome(request):
    faculty= PendingFaculty.objects.all()
    faculty2= PendingFaculty.objects.all()
    for detail in faculty:
        fac=Faculty(ID=detail.ID,password=detail.password,name=detail.name,email=detail.email,phone=detail.phone,address=detail.address,dob=detail.dob,institute=detail.institute,department=detail.department)
        fac.save()
        detail.delete()
    course_data={
        "faculty" : faculty2,
    }
    return render_to_response('app/adminhome.html',course_data)

@user_passes_test(isFaculty,login_url = '/login/faculty')
def facultyhome(request):
    print request.user.username
    faculty= Faculty.objects.get(email=request.user.username)
    course=Course.objects.filter(faculty=faculty)
    mails=Notif.objects.filter(notif_to_id=faculty.ID).filter(notif_to_role='F')
    course_data = {
           "name" : request.user.username,
           "course_list" : course,
           "mail" : mails,
    }

    return render_to_response('app/facultyhome.html',course_data)





@user_passes_test(isFaculty,login_url = '/login/faculty')
def edit_course(request,cid):
    print "YOOOOOO"
    if request.method=='POST':
        form = CalendarForm(request.POST)
        if form.is_valid():
            print "POOOOOOOOOO"
            course=Course.objects.get(course_id=cid)
            edit=form.save(commit=False)
            edit.course=course
            edit.save()
            return HttpResponseRedirect('/facultyhome')  
    else:
        print "COOOOOOOOOOOOOOO"
        form = CalendarForm()
        context = {
        "form": form,
        }
        #print render(request,"app/editcourse.html",context)
        return render(request,"app/editcourse.html",context)


@user_passes_test(isStudent,'/')
def RegInCourse(request,cid):
    course = Course.objects.get(course_id=cid)
    print "type(cid) = " + str(type(cid)) + "course = ",
    print course 
    stud = Student.objects.get(email=request.user.username)
    print "stud = ",
    print stud 
    course.student.add(stud)
    return HttpResponseRedirect('/studenthome')



def courses(request):
    courses_offered = Course.objects.all()
    course_data={
        "course" : courses_offered,
    }
    return render_to_response('app/course.html',course_data)

def course(request, num):
    print num
    course = Course.objects.get(course_id=num)
    calendar = Calendar.objects.filter(course=course)   
    course_data={
        "course" : course,
        "calendar" : calendar,
    }
    for detail in calendar:
        print detail.content
    return render_to_response('app/coursedetail.html',course_data)

def faculty(request):
    faculty = Faculty.objects.all()
    faculty_data={
        "faculty" : faculty,
    }
    return render_to_response('app/faculty.html',faculty_data)

# def addContent(request,cid):
#     user = request.user
#     QuestionFormSet = formset_factory(Question,formset=BaseQuestionFormSet)
#     if request.method == 'POST':
#         calendar_form = CalendarForm(request.POST)
#         question_formset = QuestionFormSet(request.POST)

#         if calendar_form.is_valid() and question_formset.is_valid():
#             # Save user info
#             # user.first_name = calendar_form.cleaned_data.get('date')
#             # user.last_name = calendar_form.cleaned_data.get('content')
#             cobj = calendar_form.save(commit=False)
#             cobj.save()
#             cours = Course.objects.get(course_id=cid)
#             cobj.course.add(cours)

#             # Now save the data for each form in the formset
#             new_questions = []

#             for question_form in question_formset:
#                 text = question_form.cleaned_data.get('anchor')
#                 url = question_form.cleaned_data.get('url')


#                 obj = question_form.save(commit=False)
#                 calobj = calendar_form.save(commit=False)
#                 print request.user.username
#                 fac = Faculty.objects.get(email = request.user.username)
#                 print fac
#                 obj.save()
#                 obj.calendar.add(calobj)
#                 obj.save()


            # try:
            #     with transaction.atomic():
            #         #Replace the old with the new
            #         UserLink.objects.filter(user=user).delete()
            #         UserLink.objects.bulk_create(new_links)

            #         # And notify our users that it worked
            #         messages.success(request, 'You have updated your profile.')

            # except IntegrityError: #If the transaction failed
            #     messages.error(request, 'There was an error saving your profile.')
            #     return redirect(reverse('profile-settings'))

    # else:
    #     calendar_form = CalendarForm()
    #     question_formset = QuestionFormSet()

    # context = {
    #     'profile_form': calendar_form,
    #     'link_formset': question_formset,
    # }

    # return render(request, 'app/course_content.html', context)


# class AddContentView(CreateView):
#     template_name = 'create_content.html'
#     form_class = ContentForm

#     def get_context_data(self, **kwargs):
#         context = super(AddContentView, self).get_context_data(**kwargs)
#         if self.request.POST:
#             context['formset'] = QuestionFormSet(self.request.POST)
#         else:
#             context['formset'] = QuestionFormSet()
#         return context

#     def form_valid(self, form):
#         context = self.get_context_data()
#         formset = context['formset']
#         if formset.is_valid():
#             self.object = form.save()
#             formset.instance = self.object
#             formset.save()
#             return redirect(self.object.get_absolute_url())  # assuming your model has ``get_absolute_url`` defined.
#         else:
#             return self.render_to_response(self.get_context_data(form=form))
from django.shortcuts import render, render_to_response , HttpResponse
from forms import *
from models import *
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
    HttpResponseRedirect('/')
    # Redirect to a success page.

def isStudent(user):
    try:
        stud = Student.objects.get(email=user.username)
        if stud is not None:
            return True
        return False
    except:
        return False

# @user_passes_test(isStudent,login_url = '/login/student/')
# def studenthome(request):
#     if request.method == 'POST':
#         registered_courses = Course.objects.filter(student__email = 'xyz')
#         courses_offered = Course.objects.all()
#         course_info = Calendar.objects.raw('Select * from Calendar where Calendar.course_id in ( select course_id from registered_courses) and Calender.date > datetime.now()')
#         course_data = {
#                "course_list" : registered_courses,
#                "course_offered_list" : courses_offered,
#                 "course_calendars"    : course_info,
#         }
    
#     return render_to_response('app/home.html', context_instance=RequestContext(request))


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
    students= Student.objects.filter(email=request.user.username)
    registered_courses = Course.objects.filter(student=students)
    courses_offered = Course.objects.all()
    course_info = Calendar.objects.filter(course=registered_courses)
    course_data = {
            "name" : request.user.username,
           "course_list" : registered_courses,
           "course_offered_list" : courses_offered,
            "course_calendars"    : course_info,
    }

    return render_to_response('app/studenthome.html',course_data)

@user_passes_test(isFaculty,login_url = '/login/faculty')
def facultyhome(request):
    print request.user.username
    faculty= Faculty.objects.filter(email=request.user.username)
    course=Course.objects.filter(faculty=faculty)

    course_data = {
           "name" : request.user.username,
           "course_list" : course,
    }

    return render_to_response('app/facultyhome.html',course_data)


@user_passes_test(isFaculty,'/')
def addContent(request,cid):
    try:
        fac = Faculty.objects.filter(course__course_id=cid).filter(email=request.user.username)
        if fac is not None:
            print "******************************************************************Course and Faculty match : Can edit course******************************************************************"
            
            if request.method=='POST':
                form1 = ContentForm(request.POST)
                form2 = QuestionForm(request.POST)
                #Add to database
            else:
                form = ContentForm()
                #do something else
            course_data = {
                #add info
                "heading" : "Edit Course"
            } 
            return render_to_response('app/edit_course.html',course_data)
        else:
            return HttpResponseRedirect('/')
    except:
        return HttpResponseRedirect('/')


@user_passes_test(isFaculty,'/')
def edit_course(request,cid):
    try:
        fac = Faculty.objects.filter(course__course_id=cid).filter(email=request.user.username)
        if fac is not None:
            print "******************************************************************Course and Faculty match : Can edit course******************************************************************"
            course_data = {
                #add info
                "heading" : "Edit Course"
            } 
            return render_to_response('app/edit_course.html',course_data)
        else:
            return HttpResponseRedirect('/')
    except:
        return HttpResponseRedirect('/')
    
@user_passes_test(isStudent,'/')
def RegInCourse(request,cid):
    course = Course.objects.get(course_id=cid)
    print "type(cid) = " + str(type(cid)) + "course = ",
    print course 
    stud = Student.objects.get(email=request.user.username)
    print "stud = ",
    print stud 
    course.student.add(stud)
    return HttpResponseRedirect('/')



def courses(request):
    courses_offered = Course.objects.all()
    course_data={
        "course" : courses_offered,
    }
    return render_to_response('app/course.html',course_data)

def course(request, num):
    print num
    course = Course.objects.filter(course_id=num)
    print course
    course_data={
        "course" : course,
    }
    return render_to_response('app/course.html',course_data)

def faculty(request):
    faculty = Faculty.objects.all()
    faculty_data={
        "faculty" : faculty,
    }
    return render_to_response('app/faculty.html',faculty_data)

def addContent(request,cid):
    user = request.user
    QuestionFormSet = formset_factory(Question,formset=BaseQuestionFormSet)
    if request.method == 'POST':
        calendar_form = CalendarForm(request.POST)
        question_formset = QuestionFormSet(request.POST)

        if calendar_form.is_valid() and question_formset.is_valid():
            # Save user info
            # user.first_name = calendar_form.cleaned_data.get('date')
            # user.last_name = calendar_form.cleaned_data.get('content')
            cobj = calendar_form.save(commit=False)
            cobj.save()
            cours = Course.objects.get(course_id=cid)
            cobj.course.add(cours)

            # Now save the data for each form in the formset
            new_questions = []

            for question_form in question_formset:
                text = question_form.cleaned_data.get('anchor')
                url = question_form.cleaned_data.get('url')


                obj = question_form.save(commit=False)
                calobj = calendar_form.save(commit=False)
                print request.user.username
                fac = Faculty.objects.get(email = request.user.username)
                print fac
                obj.save()
                obj.calendar.add(calobj)
                obj.save()


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

    else:
        calendar_form = CalendarForm()
        question_formset = QuestionFormSet()

    context = {
        'profile_form': calendar_form,
        'link_formset': question_formset,
    }

    return render(request, 'app/course_content.html', context)


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
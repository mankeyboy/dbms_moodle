"""coursera URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
	url(r'^$','app.views.home'),
    url(r'^logout/','app.views.logout_view'),
    url(r'^admin/', admin.site.urls),
    url(r'^signup/',include('app.urls')),
    url(r'^login/','app.views.login_user'),
    url(r'^adminhome/','app.views.adminhome',name='adminhome'),
    url(r'^facultyhome/','app.views.facultyhome',name='facultyhome'),
    url(r'^studenthome/','app.views.studenthome',name='studenthome'),
    url(r'^offercourse/','app.views.offerCourse',name='offercourse'),
    url(r'^student/','app.views.studentSignUp',name = 'studentSignUp'),
    url(r'^faculty/','app.views.faculty',name = 'facultySignUp'),
    url(r'^course/(\d+)/','app.views.course',name='course'),
    url(r'^courses/','app.views.courses',name='courses'),
    url(r'^faculty_detail/','app.views.faculty',name='faculty'),
    url(r'^register/(\d+)/','app.views.RegInCourse',name='RegInCourse'),
    url(r'^edit/(\d+)/','app.views.edit_course',name='edit_course'),
    url(r'^sendmail/','app.views.sendmail',name='sendmail'),
    url(r'^quizform/','app.views.quizform',name='quizform'),
    url(r'^shownotif/','app.views.shownotif',name='notif'),
    url(r'^about/','app.views.about',name='about'),
    url(r'^contact/','app.views.contact',name='contact'),
    url(r'^parent/','app.views.parent',name='parent'),
    # url(r'^create_content/(\d+)/','app.views.addContent',name='addContent'),
]

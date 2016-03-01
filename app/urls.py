from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
	url(r'^login/','app.views.login_user',name = 'login_user'),
	# url(r'^$','app.views.studentSignUp',name = 'studentSignUp'),
	url(r'^student/','app.views.studentSignUp',name = 'studentSignUp'),
	url(r'^faculty/','app.views.facultySignUp',name = 'facultySignUp'),
	)
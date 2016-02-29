from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
	url(r'^login/','app.views.loginStudent',name = 'loginStudent'),
	# url(r'^$','app.views.studentSignUp',name = 'studentSignUp'),
	# url(r'^signup/','app.views.studentSignUp',name = 'studentSignUp'),
	)
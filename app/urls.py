from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
	url(r'^$','app.views.gaaliDe',name = 'gaaliDe'),
	url(r'^signup/','app.views.gaaliDe',name = 'gaaliDe'),
	)
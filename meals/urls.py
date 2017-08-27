from django.conf.urls import patterns, url
from meals import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	url(r'^(?P<meal_id>[\d]+)/$', views.index, name='index'),
)

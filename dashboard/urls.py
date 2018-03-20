from django.conf.urls import url
from dashboard import views

app_name = 'dashboard'

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^histogram/$', views.histogram, name='histogram'),
	url(r'^piechart/$', views.piechart, name='piechart'),
	url(r'^linegraph/$', views.linegraph, name='linegraph'),
]
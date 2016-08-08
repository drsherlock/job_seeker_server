from django.conf.urls import url

from Jobs import views

urlpatterns = [
    url(r'^companies/api/$', views.get_companies),
    url(r'^jobs/api/$', views.get_jobs),
    url(r'^companies/(?P<id>\d+)/api/$', views.get_company),
    url(r'^companies/search/(?P<company>[\w\-]+)/api/$', views.search_companies),
    url(r'^jobs/search/(?P<job>[\w\-]+)/api/$', views.search_jobs),
    # url(r'^jobs/(?P<id>\d+)/$', views.get_job)

]

from django.conf.urls import url

from Jobs import views

urlpatterns = [
    url(r'^companies/$', views.get_companies),
    url(r'^jobs/$', views.get_jobs),
    url(r'^companies/(?P<id>\d+)/$', views.get_company),
    # url(r'^jobs/(?P<id>\d+)/$', views.get_job)

]

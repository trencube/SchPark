from django.conf.urls import url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings

from core.views import DashboardView, SparkConsoleView, JobsView, NewJobView, JobView


urlpatterns = [
    url(r'^login/', 'django.contrib.auth.views.login', {'template_name': 'core/login.html'}),
    url(r'^logout/', 'django.contrib.auth.views.logout', {'next_page': '/login'}),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),

    url(r'^$', DashboardView.as_view()),
    url(r'^spark_console/$', SparkConsoleView.as_view()),
    url(r'^new_job/$', NewJobView.as_view()),
    url(r'^jobs/$', JobsView.as_view()),
    url(r'^job/(?P<job_id>[0-9]+)/$', JobView.as_view()),
    url(r'^job/disable_job/(?P<job_id>[0-9]+)/$', 'core.views.disable_job'),
    url(r'^job/enable_job/(?P<job_id>[0-9]+)/$', 'core.views.enable_job'),
    url(r'^job/delete_job/(?P<job_id>[0-9]+)/$', 'core.views.delete_job'),
]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()

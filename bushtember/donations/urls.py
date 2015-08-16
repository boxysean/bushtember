from django.conf.urls import patterns, url

from . import views


urlpatterns = patterns('',
    url(r'^$', views.demo_view),
    url(r'^upload$', views.demo_upload_view),
)

from django.conf.urls import patterns, url

from . import views


urlpatterns = patterns('',
    url(r'^$', views.donate_view),
    url(r'^upload/$', views.upload_photo_view),
    url(r'^upload/(?P<upload_token_value>\w+)/$', views.upload_photo_view),
)

from django.conf.urls import patterns, url

from . import views


urlpatterns = patterns('',
    url(r'^$', views.donate_view),
    url(r'^test/$', views.test_view),
    url(r'^donation/$', views.upload_photo_view),
    url(r'^donation/(?P<donation_token>\w+)/$', views.upload_photo_view),
)

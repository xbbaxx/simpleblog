from django.conf.urls import patterns, include, url
from . import views


urlpatterns = patterns('',
    url(r'^$', views.Index),
    url(r'^post/(?P<pk>[0-9]+)/$', views.post_detail),
    url(r'^post/new/$', views.post_new, name="post_new"),
    url(r'^post/edit/(?P<pk>[0-9]+)/$', views.post_edit, name='post_edit')
)

from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns
from api import views
from api import tests
from api.entry_point import request_stack

urlpatterns = [
    url(r'^/test$', tests.test_main),
    url(r'^/query$', request_stack),
    url(r'^$', views.list_features),
    url(r'^/$', views.list_features),
]
#    url(r'^api/(?P<pk>[0-9]+)$', views.snippet_detail),

urlpatterns = format_suffix_patterns(urlpatterns)

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import patterns, url

from .views import html_page

urlpatterns = patterns('',
    url(r'', html_page, name='html_page'),
)

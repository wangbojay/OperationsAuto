"""OperationsAuto URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from OA.views import *
import settings
from django.views.static import serve
from django.contrib.auth.views import login,logout_then_login
import xadmin
xadmin.autodiscover()

urlpatterns = [
    url(r'^admin/', include(xadmin.site.urls)),
    url(r'^$', index),
    url(r'^accounts/login/$', login),
    url(r'^accounts/logout/$', logout_then_login),
    url(r'^pj', pj),
    url(r'^server', server),
    url(r'^database', database),
    url(r'^quick_task', quick_task),
    url(r'^custom_task', custom_task),
    url(r'^monitor_graph_pj_select$', monitor_graph_select),
    url(r'^monitor_graph', monitor_graph),
    url(r'^monitor_table', monitor_table),
    url(r'^info_collect', info_collect),
]

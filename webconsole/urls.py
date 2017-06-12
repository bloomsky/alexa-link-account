
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^login/$', views.login.as_view(),  name='login'),
    url(r'^fb_login/$', views.fb_login.as_view(), name='fb_login'),
    ]

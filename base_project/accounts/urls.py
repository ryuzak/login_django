from django.conf.urls import include, url
from . import views

urlpatterns = [
    #-- Accounts
    url(r'^users/$', views.users_list.as_view(), name="users_list"),
    url(r'^users/add/$', views.users_add, name="users_add"),
    url(r'^users/(?P<pk>[0-9]+)/edit/$', views.users_edit, name="users_edit"),
    url(r'^users/(?P<pk>[0-9]+)/changepassword/$', views.users_changepassword, name="users_changepassword"),
    url(r'^users/(?P<pk>[0-9]+)/delete/$', views.users_delete, name="users_delete"),
]


from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.account_dashboard, name="dashboard"),
    url(r'^login/$', views.account_login, name="login"),
    url(r'^logout/$', views.account_logout, name="logout"),
]
from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^users/email/request/([0-9]{1})/$', views.users_email, name="users_email"),
    url(r'^users/activation/(?P<activation_key>\w+)/$', views.users_activation, name="users_activation"),
    url(r'^users/recoverypassword/(?P<recovery_key>\w+)/$', views.users_recoverypassword, name="users_recoverypassword"),
]

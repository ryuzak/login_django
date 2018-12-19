from django.conf.urls import include, url
from . import views

urlpatterns = [
	url(r'^list/$',views.customer_list,name="customer_list"),
	url(r'^add/$',views.customer_add,name="customer_add"),
	url(r'^(?P<customer_id>[0-9]+)/edit/$',views.customer_edit,name="customer_edit"),
	url(r'^(?P<customer_id>[0-9]+)/delete/$',views.customer_delete,name="customer_delete"),
]

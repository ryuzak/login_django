# -*- encoding: utf-8 -*-
from django.shortcuts import render, redirect, get_object_or_404, Http404

#-- Models
from .models import Customer

#-- Forms
from .forms import CustomerForm

#-- Functions
import base_project.functions as fn


def customer_list(request):
	try:
		customers = Customer.objects.filter(status=1)
	except Exception as e:
		customers = None
	return render(request, 'customers/customers_list.html', {'customers':customers})


def customer_add(request):
	form = CustomerForm(request.POST or None)
	print(form)
	if form.is_valid():
		customer_model = form.save(commit=False)
		customer_model.createdby_id = fn.get_user_id(request)

		customer_model.save()
		return redirect('accounts:users_add')
	
	return render(request, 'customers/customer_add.html',{'form':form})


def customer_edit(request, customer_id):
	try:
		customer = Customer.objects.get(pk=customer_id, status=1)
	except Exception as e:
		raise Http404

	form = CustomerForm(request.POST or None, instance=customer)
	if(form.is_valid()):
		customer = form.save(commit=False)
		customer.area_adquired = form.cleaned_data.get('area_adquired')
		customer.modifiedby_id = fn.get_user_id(request)
		customer.save()
		return redirect('customers:customer_list')
	
	return render(request, 'customers/customer_add.html',{'form':form})


def customer_delete(request, customer_id):
	try:
		customer = Customer.objects.get(pk=customer_id, status=1)
		customer.status=-1
		customer.modifiedby_id = fn.get_user_id(request)
		customer.save()
	except Exception as e:
		raise Http404
	return redirect('customers:customer_list')



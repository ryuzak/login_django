# -*- encoding: utf-8 -*-
from django.contrib.auth.decorators import user_passes_test, login_required
from django.shortcuts import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import Group
from customers.models import Customer

#funciones lambda para verificacion de pertenencia a un grupo de cliente
is_superuser = lambda x: Group.objects.get(name="SuperAdmin") in x.groups.all()
is_basic = lambda x: Group.objects.get(name="basic") in x.profile.all()
is_agroclima = lambda x: Group.objects.get(name="customer_agroclima") in x.profile.all()
is_drone = lambda x: Group.objects.get(name="customer_drone") in x.profile.all()
is_full = lambda x: Group.objects.get(name="customer_full") in x.profile.all()


def validate_customer_full(customer):
    return is_full(customer)

def validate_customer_drone(customer):
    return is_drone(customer)

def validate_customer_agroclima(customer):
    return is_agroclima(customer)

def validate_customer_basic(customer):
    return is_basic(customer)

def validate_super_admin(customer):
    return is_superuser(customer)

def check_profile(condition=None, function=None, home_url=None, redirect_field_name=None): 
    #settear url si no se ha proporcionado una
    #print condition
    if home_url is None:
        home_url = '/'

    #funcion del decorador, recibe la vista como paramatetro
    def _dec(view_func):
        #funcion de vista, recibe request como parametro principal, args y kwargs como parametros opcionales
        def _view(request, *args, **kwargs):
            if(condition == '0'):
                if(validate_super_admin(request.user)):
                    return view_func(request, *args, **kwargs)
                else:
                    return HttpResponseRedirect(home_url)
            elif(condition == '1'):
                return view_func(request, *args, **kwargs)
            elif(condition == '2'):
                customer = Customer.objects.get(users__id=request.user.id)
                if(customer.profile.name=='customer_full' or customer.profile.name=='customer_agroclima'):
                    return view_func(request, *args, **kwargs)
                else:
                    return HttpResponseRedirect(home_url)
            elif(condition == '3'):
                customer = Customer.objects.get(users__id=request.user.id)
                if(customer.profile.name=='customer_full' or customer.profile.name=='customer_drone'):
                    return view_func(request, *args, **kwargs)
                else:
                    return HttpResponseRedirect(home_url)
            else:
                return HttpResponseRedirect(home_url)
        #paso de propiedades de la vista a la funcion para la vista
        _view.__name__ = view_func.__name__
        _view.__dict__ = view_func.__dict__
        _view.__doc__ = view_func.__doc__

        #regresa la vista
        return _view

    #regresa el decorador
    if function is None:
        return _dec
    else:
        return _dec(function)


def check_profile_async(condition=None, function=None, default_response=None, redirect_field_name=None): 
    #settear url si no se ha proporcionado una
    if default_response is None:
        default_response = 'false'
    #funcion del decorador, recibe la vista como paramatetro
    def _dec(view_func):
        
        #funcion de vista, recibe request como parametro principal, args y kwargs como parametros opcionales
        def _view(request, *args, **kwargs):
            customer = Customer.objects.get(users__id=request.user.id)
            if(condition == '1'):
                return view_func(request, *args, **kwargs)
            elif(condition == '2'):
                if(customer.profile.name=='customer_full' or customer.profile.name=='customer_agroclima'):
                    return view_func(request, *args, **kwargs)
                else:
                    return HttpResponse(default_response)
            elif(condition == '3'):
                if(customer.profile.name=='customer_full' or customer.profile.name=='customer_drone'):
                    return view_func(request, *args, **kwargs)
                else:
                    return HttpResponse(default_response)
            else:
                return HttpResponse(default_response)
        #paso de propiedades de la vista a la funcion para la vista
        _view.__name__ = view_func.__name__
        _view.__dict__ = view_func.__dict__
        _view.__doc__ = view_func.__doc__

        #regresa la vista
        return _view

    #regresa el decorador
    if function is None:
        return _dec
    else:
        return _dec(function)




# -*- encoding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
#-- Auth
from django.contrib.auth import authenticate, login, logout

#-- Forms
from .forms import LoginForm
from recovery.forms import EmailForm

#-- Models
from accounts.models import User

#-- Functions
import base_project.functions as func



# Create your views here.
#-- User Iniciar Sesion
def account_login(request):
    message = ''
    email_form = ''
    if request.method == 'POST':

        login_form = LoginForm(request.POST)
        email_form = LoginForm()

        if login_form.is_valid():
            user = authenticate(email=login_form.cleaned_data.get('email'), password=login_form.cleaned_data.get('password'))

            if user:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect('/')
                else:
                    message = 'Correo o contraseña no validos'
            else:
                message = 'Correo o contraseña no validos'
        else:
            message= 'Datos incorrectos'
    else:
        login_form = LoginForm()
        email_form = EmailForm()

    return render(request, 'authorization/login.html',{'form': login_form, 'formail' : email_form, 'message' : message})


#-- Logout
def account_logout(request):
    logout(request)
    # Take the user back to the login
    return HttpResponseRedirect('/login')

#-- Dashboard
def account_dashboard(request):
    if request.user.is_authenticated():
        #customer = request.user.customer_set.get(users__id=request.user.id)
        return render(request, 'authorization/dashboard.html',{
         #   'customer':customer,
        })
    else:
       return HttpResponseRedirect('login/')




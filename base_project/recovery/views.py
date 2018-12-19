# -*- encoding: utf-8 -*-
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.http import Http404

#-- Importar Funciones generales
from django.utils import timezone
import datetime

#-- Forms
from .forms import PasswordForm, EmailForm, EmailRecoveryForm

#-- Models
from accounts.models import User, UserRequest

#-- Functions
import base_project.functions as func

#-- Sendmail - Solicitar Correo (1: Activacion, 2:Recuperar contraseña)
def users_email(request, typemail):
    message = ''
    subject = {'1': 'Activar Cuenta', '2' : 'Recuperar Contraseña'}
    header = {'1' : 'Solicitar Correo de Activación', '2' : 'Solicitar Correo de Recuperación de Contraseña'}

    if request.method == 'POST':
        
        if typemail == '1': 
            email_form = EmailForm(request.POST)
        else:
            email_form = EmailRecoveryForm(request.POST)
        
        if email_form.is_valid():
            email = email_form.cleaned_data['email']

            userid = User.objects.get(email=email)

            func.sendmail_activations(request, email, userid, typemail)            

            return render(request, 'recovery/users_sendmail.html', {'message' : message, 'header' : subject[typemail]})
    else:
        if typemail == '1': 
            email_form = EmailForm()
            message = 'El link de activación ha expirado. Por favor solicita otro.'
        else:
            email_form = EmailRecoveryForm()
            message = 'Introduzca su correo. En breve se enviara un link para la recuperación de su contraseña'
        
    return render(request, 'recovery/users_email.html', {'form' : email_form, 'message' : message, 'header' : header[typemail]})
    

#-- User Confirmar cuenta y capturar contraseña
def users_activation(request, activation_key):
    message = ''
    #-- Si la Activation no ha expirado, entonces capturamos la contraseña y cambiamos el valor de is_activate=True
    if request.method == 'POST':
        
        #-- Campos de la forma de acivacion de usuario
        activation_form = PasswordForm(request.POST)       
        if activation_form.is_valid():

            password_activation = activation_form.cleaned_data.get('password')
            password_activation2 = activation_form.cleaned_data.get('password2')
            useridkey = User.objects.get(userrequest__activation_key=activation_key)
            #-- Guardamos la contraseña y activamos el usuario 
            useridkey.set_password(password_activation)
            
            urequest = UserRequest.objects.get(activation_key=activation_key)
            urequest.activation_status = '1'
            urequest.save()
            
            useridkey.is_active = True
 			#-- Campos de control
            useridkey.modifiedby_id = useridkey.id
            useridkey.last_modified_date = datetime.datetime.now()  
            useridkey.status = 1
            useridkey.save()
    
            return render(request, 'recovery/users_recovery_success.html',  {'header' : 'Cuenta activada', 'message' : 'Su cuenta ha sido activada. Por favor inicie sesión en el siguiente enlace'})
    else:
         #-- Validar si la activation key es igual a la que tiene the activation key (Si no le mandamos un error 404)
        try:
        
            user_request = UserRequest.objects.get(activation_key=activation_key)
        except Exception as e:
            raise Http404()            
        #-- Validar isi la activation key no ha expirado, si es asi, mandamos un mensaje de error
        if user_request.activation_status == '-1' or user_request.activation_status == '1':
            
            message = 'El link de activación ha expirado. Por seguridad, solicite otro.'
            
            #-- Solicitar un nuevo correo de activacion
            return HttpResponseRedirect(reverse('recovery:users_email', args=[1]))
        
        elif user_request.expires_key < timezone.now():
            message = 'El link de activación ha expirado. Por seguridad, solicite otro.'
                
            #-- Status de expirado a la activacion key
            user_request.activation_status = '-1'
                
            user_request.save()

            #-- Solicitar un nuevo correo de activacion
            return HttpResponseRedirect(reverse('recovery:users_email', args=[1]))
    
    activation_form = PasswordForm()
    
    return render(request, 'recovery/users_password.html', {'form' : activation_form, 'message' : message, 'header' : 'Activar Cuenta'})

#-- Recuperar contraseña por correo
def users_recoverypassword(request, recovery_key):          
    message = ''
    #-- Si la Activation no ha expirado, entonces capturamos la contraseña
    if request.method == 'POST':
        
        password_form = PasswordForm(request.POST)
        
        if password_form.is_valid():
            
            password_change = password_form.cleaned_data.get('password')
            password_change2 = password_form.cleaned_data.get('password2')
            
            useridkey = User.objects.get(userrequest__activation_key=recovery_key)
                        
            #-- Guardamos la contraseña
            useridkey.set_password(password_change)
            
            urequest = UserRequest.objects.get(activation_key=recovery_key)
            urequest.activation_status = '1'
           
            useridkey.userrequest = urequest
            useridkey.userrequest.save()            
            
 			
            #-- Campos de control
            useridkey.modifiedby_id = useridkey.id
            useridkey.last_modified_date = datetime.datetime.now()  
            
            useridkey.save()
    
            return render(request, 'recovery/users_recovery_success.html',  {'header' : 'Contraseña reestablecida', 'message' : 'Su contraseña ha sido reestablecida. Por favor inicie sesión en el siguiente enlace'})

    else:
         #-- Validar si la activation key es igual a la que tiene the activation key (Si no le mandamos un error 404)
        user_request = get_object_or_404(UserRequest, activation_key=recovery_key)

        #-- Validar isi la activation key no ha expirado, si es asi, mandamos un mensaje de error
        if user_request.activation_status == '-1' or user_request.activation_status == '1':
            message = 'El link de recuperación de contraseña ha expirado. Por seguridad, solicite otro.'
            
            #-- Solicitar un nuevo correo de recuperacion
            return HttpResponseRedirect(reverse('recovery:users_email', args=[2]))
        
        else:
            if user_request.expires_key < timezone.now():
                message = 'El link de recuperación de contraseña ha expirado. Por seguridad, solicite otro.'
                
                #-- Status de expirado a la activacion key
                user_request.activation_status = '-1'
                
                user_request.save()
           
                #-- Solicitar un nuevo correo de recuperacion
                return HttpResponseRedirect(reverse('recovery:users_email', args=[2]))
            
    password_form = PasswordForm()
    
    return render(request, 'recovery/users_password.html', {'form' : password_form, 'message' : message, 'header' : 'Recuperar Contraseña'})
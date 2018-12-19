# -*- encoding: utf-8 -*-
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
#-- Importar Funciones generales
import datetime
#-- Generic Views
from django.views.generic import ListView
#-- Forms
from .forms import UserForm, ChangepasswordForm
#-- Models
from customers.models import Customer
from accounts.models import User
#-- Functions
import base_project.functions as func

#-- User Lista de usuarios
class users_list(ListView):
    context_object_name = "users_list"
    template_name = "accounts/users_list.html"

    def get_queryset(self):
        #customer_id = func.get_customer_id(self.request)
        #customer = Customer.objects.get(pk=customer_id)
        return User.objects.all().order_by('-first_name')

def users_add(request):
    if request.method == 'POST':
        #-- Campos de la forma de registro de usuario
        user_form = UserForm(request.POST, user=request.user)
        if user_form.is_valid():
            validation = User.objects.filter(email__iexact=user_form.cleaned_data.get('email')).exclude(email__iexact=user_form.cleaned_data.get('email'))
            if validation:
                email_user = User.objects.get(emal=email)
                if email_user.email == email and email_user.status == '-1':
                    user_form.save(update_fields=[user_form])
                    User.objects.filter(pk=email_user.pk).update(status='1')
                    if(user_form.cleaned_data.get('user_type') != 'NA'):
                        #-- Creamos las llaves de activacion
                        func.sendmail_activations(request, user_form.cleaned_data.get('email'), user_model, '1')
            user_model = user_form.save()
            if 'picture' in request.FILES:
                user_model.picture = request.FILES['picture']
            #-- Campos de control
            user_model.createdby_id = func.get_user_id(request)
            user_model.status='-1'
            user_model.save()
            #-- Relacion many to many con a tabla customer_users
            # customer_id = func.get_customer_id(request)
            # customer = Customer.objects.get(pk=customer_id)
            # customer.users.add(user_model.id)
            #-- Si el usuario es personal con acceso al sistema
            if(user_form.cleaned_data.get('user_type') != 'NA'):
                #-- Creamos las llaves de activacion
                func.sendmail_activations(request, user_form.cleaned_data.get('email'), user_model, '1')
            #-- Redireccionamos a la lista de usuarios
            return redirect('accounts:users_list')
    else:
        user_form = UserForm(user=request.user)
    return render(request, 'accounts/users_form.html', {'form' : user_form, 'header' : 'Agregar Usuario'})

#-- User Modificar Perfil Usuario
def users_edit(request, pk):
    userid = get_object_or_404(User, pk=pk)
    user_form = UserForm(request.POST or None, instance=userid, user=request.user)
    if user_form.is_valid():
        user_model = user_form.save(commit=False)
        if 'picture' in request.FILES:
            user_model.picture = request.FILES['picture']
			#-- Campos de control
        user_model.modifiedby_id = func.get_user_id(request)
        user_model.last_modified_date = datetime.datetime.now()
        user_model.save()
        return redirect('cust_field:field_list')
    
    return render(request, 'accounts/users_form.html', {'form' : user_form, 'image' : userid, 'header':'Modificar Usuario'})


#-- User Cambiar Contraseña
def users_changepassword(request, pk):
    #-- Campos de la forma de cambio de contraseña
    changepassword_form = ChangepasswordForm(request.POST or None, user=request.user)
    userid = get_object_or_404(User, pk=pk)
    if changepassword_form.is_valid():
        password_change = changepassword_form.cleaned_data.get('password')
        password_change2 = changepassword_form.cleaned_data.get('password2')
        #-- Guardamos la nueva contraseña
        userid.set_password(password_change)
			#-- Campos de control
        userid.modifiedby_id = func.get_user_id(request)
        userid.last_modified_date = datetime.datetime.now()
        userid.save()
        return redirect('accounts:users_list')
    return render(request, 'accounts/users_password_change.html', {'form' : changepassword_form, 'currentpass' : '1', 'header':'Cambiar Contraseña'})

#-- Eliminar Usuario (Desactivar)
def users_delete(request, pk):
    try:
        customer_id = func.get_customer_id(request)
        customer = Customer.objects.get(pk=customer_id)
        user_delete = User.objects.get(pk=pk)
        customer.users.remove(user_delete)
        user_count = Customer.objects.filter(users__pk=pk).count()
        if(user_count == 0):
            user_delete.status = -1
            user_delete.is_active = False
        user_delete.modifiedby_id = func.get_user_id(request)
        user_delete.deleted_date = datetime.datetime.now()
        user_delete.save()
    except (KeyError, customer.DoesNotExist):
        return render(request,'aaccounts/users_list.html', {'message':'Ocurrio un error al eliminar usuario'})
    return redirect('accounts:users_list')

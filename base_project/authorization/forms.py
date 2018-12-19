# -*- encoding: utf-8 -*-
from django import forms
from django.forms import ModelForm
#from django.contrib.auth.models import User
#from .models import User

#-- Functions
#import jondatron.functions as func


#-- Import utilies
#import jondatron.utilies as ut

#-- Login form
class LoginForm(forms.Form):

    email = forms.EmailField(
        label = 'E-Mail',
        error_messages = {'required':'Ingrese un correo valido'},
        widget = forms.TextInput(
            attrs={
                'class': 'form-control form-control-solid placeholder-no-fix',
                'placeholder' : 'E-Mail'
            }
        )
    )

    password = forms.CharField(
        label = 'Contraseña',
        widget = forms.PasswordInput(
            attrs={
                'class': 'form-control form-control-solid placeholder-no-fix',
                'placeholder' : 'Contraseña'
            }
        )
    )

    class Meta:
        fields = ('email', 'password',)
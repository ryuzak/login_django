# -*- encoding: utf-8 -*-
from django import forms
from django.forms import ModelForm
#from django.contrib.auth.models import User
from accounts.models import User

##-- User Password form
class PasswordForm(forms.Form):
    password = forms.CharField(
        label = 'Contraseña',
        widget = forms.PasswordInput(
            attrs={
                'class': 'form-control form-control-solid placeholder-no-fix',
                'placeholder' : 'Contraseña'
            }
        )
    )
    
    password2 = forms.CharField(
        label = 'Confirmar Contraseña',
        widget = forms.PasswordInput(
            attrs={
                'class': 'form-control form-control-solid placeholder-no-fix',
                'placeholder' : 'Confirmar Contraseña'
            }
        )
    )
    
    def clean_password2(self):
        #-- Comprueba que password y password2 sean iguales.
        password = self.cleaned_data['password']
        password2 = self.cleaned_data['password2']
        if password != password2:
            raise forms.ValidationError('Las contraseñas no coinciden.')
        return password2

    class Meta:
        fields = ('password', 'password2')
        
#-- User email form
class EmailForm(forms.Form):

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
    
    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            emailvalid = User.objects.get(email=email, status=1, is_active=False)
        except User.DoesNotExist:
            raise forms.ValidationError('Este correo no existe o la cuenta ya ha sido activada')
        return email

    class Meta:
        fields = ('email')

#-- User email form recovery
class EmailRecoveryForm(forms.Form):
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
    
    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            emailvalid = User.objects.get(email=email, status=1)
        except User.DoesNotExist:
            raise forms.ValidationError('Este correo no existe')
        return email

    class Meta:
        fields = ('email')

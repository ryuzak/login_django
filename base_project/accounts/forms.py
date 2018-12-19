# -*- encoding: utf-8 -*-
from django import forms
from django.forms import ModelForm
#from django.contrib.auth.models import User
from .models import User

#-- Import utilies
import base_project.utilies as ut

#-- User form
class UserForm(ModelForm):
    
    first_name = forms.CharField(
        label = 'Nombre',
        #error_messages = {'required':'cmapo no valido'},
        widget = forms.TextInput(
            attrs = {
                'class': 'form-control'
            }
        )
    )
    last_name = forms.CharField(
        label = 'Apellidos', 
        #error_messages = {'required':'Enter a valid phone number'},
        widget = forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )

    email = forms.EmailField(
        label = 'Correo',
        #error_messages = {'required':'Este campo es requerido', 'invalid':'correo mal'},
        widget = forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )

    picture = forms.ImageField(
        label = 'Foto',
        required = False,
        error_messages = {'invalid': "Solo archivos de imagen"},
        widget = forms.FileInput(
            attrs = {
                'class': 'form-control'
            }
        )
    )
    
    phone = forms.CharField(
        label = 'Teléfono', 
        #error_messages = {'required':'Enter a valid phone number'},
        widget = forms.TextInput(
            attrs={
                'class': 'form-control',
                'id' : 'mask_phone'
            }
        )
    )
    
    user_type = forms.CharField(
        label = 'Tipo de Usuario',
        max_length=2,
        required = False,
        #error_messages = {'required':'Este campo es requerido', 'invalid':'correo mal'},
        widget = forms.Select(
            choices=ut.USERTYPES_CHOICES,
            attrs={
                'class': 'form-control'
            }
        )
    )
    
    status = forms.MultipleChoiceField(
        label = 'Status',
        required = False,
        widget = forms.CheckboxSelectMultiple(
            choices=ut.STATUS_CHOICES,
            attrs={
                'class': 'make-switch',
                'checked' : 'true',
                'data-size' : 'small'
            }
        )
    )
    
    #-- 
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(UserForm, self).__init__(*args, **kwargs)
                                       
    def clean_email(self):
        email = self.cleaned_data['email']
        #print email

        #usermail = User.objects.filter(email__iexact=email).exclude(email__iexact=email)
        try:
            usermail = User.objects.get(email=email, status=1)
            raise forms.ValidationError('Este correo ya está registrado')
        except Exception as e:
            pass
            
        return email
        
    class Meta:
        model = User
        #fields = ('username','first_name','last_name','email','password','password2')
        fields = ('first_name','last_name','email', 'phone', 'picture', 'user_type', 'status')
    
#-- User Changepassword form
class ChangepasswordForm(forms.Form):
    currentpassword = forms.CharField(
        label = 'Contraseña Actual',
        widget = forms.PasswordInput(
            attrs={
                'class': 'form-control form-control-solid placeholder-no-fix',
                'placeholder' : 'Contraseña Actual'
            }
        )
    )
    
    
    password = forms.CharField(
        label = 'Nueva Contraseña',
#        min_length=8,
#        error_messages = {'invalid':'La cotraseña debe de contener minimo 8 caracteres'},
        widget = forms.PasswordInput(
            attrs={
                'class': 'form-control form-control-solid placeholder-no-fix',
                'placeholder' : 'Nueva Contraseña'
            }
        )
    )
    
    password2 = forms.CharField(
        label = 'Confirmar Nueva Contraseña',
        widget = forms.PasswordInput(
            attrs={
                'class': 'form-control form-control-solid placeholder-no-fix',
                'placeholder' : 'Confirmar Nueva Contraseña'
            }
        )
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ChangepasswordForm, self).__init__(*args, **kwargs)
        
    def clean_currentpassword(self):
        #-- Comprueba que password y password2 sean iguales.
        currentpassword = self.cleaned_data['currentpassword']
        
        userkey = User.objects.get(pk=self.user.id)
        
        checkpass = userkey.check_password(currentpassword)
        
        if checkpass == False:
            raise forms.ValidationError('Las contraseña actual es incorrecta.')
        
        return currentpassword
    
    def clean_password2(self):
        #-- Comprueba que password y password2 sean iguales.
        password = self.cleaned_data['password']
        password2 = self.cleaned_data['password2']
        if password != password2:
            raise forms.ValidationError('Las contraseñas no coinciden.')
        return password2

    class Meta:
        fields = ('currentpassword', 'password', 'password2')
        
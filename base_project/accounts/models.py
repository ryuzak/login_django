# -*- encoding: utf-8 -*-
from django.db import models
from base.models import BaseModel
from datetime import datetime
#-- Import User Model
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
#-- Import utilies
import base_project.utilies as ut
#--- Settings base
from base_project.settings import settings as base

#-- Upload pictures users
def user_filename(self, filename):
    url = "accounts_picture/%s/%s" % (self.id, filename)
    return url

#-- Create_user extendido de AbstractBaseUser
class UserManager(BaseUserManager):

    def create_user(self, email, password=None):
        user = self.model(
            email=self.normalize_email(email),
            is_active=False,
        )
        return user

#-- Clase abstracta extendida del modelo User
class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    email = models.EmailField(unique=True, db_index=True)
    #-- Atributos adicionales
    phone = models.CharField(max_length=10)
    picture = models.ImageField(upload_to=user_filename, blank=True)
    user_type = models.CharField(max_length=2, choices=ut.USERTYPES_CHOICES, default='A')
    api_token = models.CharField(max_length=50, default='')
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'

    objects = UserManager()

    def __unicode__(self):
        return self.first_name + ' ' + self.last_name

    class Meta:
        db_table = 'users'

#-- Clase extendia del User para control de las llaves de activacion (Activacion / Solicitud de Contraseña / Invitacion)
class UserRequest(models.Model):
    user = models.ForeignKey(base.AUTH_USER_MODEL, on_delete=models.CASCADE, unique=False)
    #-- Keys para la validacion por email cuando de crea el usuario
    activation_key = models.CharField(max_length=40, blank=True)
    expires_key = models.DateTimeField(default=datetime.now)
    activation_type = models.CharField(max_length=2, choices=ut.ACTIVATION_CHOICES, default='1')
    activation_status = models.CharField(max_length=2, choices=ut.ACTIVATIONSTATUS_CHOICES, default='0')
    activation_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'users_request'

class UserModulePermanence(models.Model):
    user = models.ForeignKey(base.AUTH_USER_MODEL, on_delete=models.CASCADE, unique=False)
    petition_type = models.CharField(max_length=50)
    url = models.CharField(max_length=256)
    ip = models.CharField(max_length=15)
    use_proxy = models.BooleanField(default=False)
    time_request_init = models.DateTimeField(auto_now_add=True)
    time_request_out = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'user_module_permanence'

class UserActions(models.Model):
    user = models.ForeignKey(base.AUTH_USER_MODEL, on_delete=models.CASCADE, unique=False)
    url = models.CharField(max_length=256)
    ip = models.CharField(max_length=15)
    action = models.CharField(max_length=256)
    time_request = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'user_actions'

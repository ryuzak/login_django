# -*- encoding: utf-8 -*-
import datetime
import unicodedata
from django.conf import settings
# from django.forms import ModelChoiceField
# import functions as fn

#-- Status Values
STATUS_CHOICES = (
    (-1, 'Eliminado'),
    (0, 'Inactivo'),
    (1, 'Activo'),
)

#-- Customer User Type Values
USERTYPES_CHOICES = (
    ('SA','Super Admin'),
    ('C','Admin Agricola'),
    ('G', 'Gerente'),
    ('TI', 'Tecnico Interno'),
    ('TE', 'Tecnico Externo'),
    ('NA', 'Sin Acceso'),
)

#-- Activation Request Values
ACTIVATION_CHOICES = (
    (1, 'Activacion'),
    (2, 'Solicitud Password'),
    (3, 'Invitacion'),
)

#-- Activation Status Values
ACTIVATIONSTATUS_CHOICES = (
    (-1, 'Expirado'),
    (0, 'Enviado'),
    (1, 'Activado'),
)

#-- State Type Values
COUNTRYTYPES_CHOICES = (
    ('1','México'),
    ('2', 'USA'),
)
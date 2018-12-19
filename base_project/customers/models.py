# -*- encoding: utf-8 -*-
from django.db import models
from base.models import BaseModel
from datetime import datetime
from django.contrib.auth.models import Group

#-- Import utilies
import base_project.utilies as ut

#--- Settings base
from base_project.settings import settings as base

#-- Upload pictures users
def customer_filename(self, filename):
    url = "customers_logo/%s/%s" % (self.customer.id, filename)
    return url

# Create your models here.

#-- Informacion general del cliente (Agricola)
class Customer(BaseModel):
    name = models.CharField(max_length=140)
    website = models.URLField(blank=True)
    phone = models.CharField(max_length=10)
    email = models.EmailField(blank=True)
    street = models.CharField(max_length=140, null=True)
    colony = models.CharField(max_length=140, null=True)
    nostreet = models.IntegerField(blank=True, default=0, null=True)
    zipcode = models.IntegerField(default=0, null=True)
    country = models.CharField(max_length=5, default='')
    logo = models.ImageField(upload_to=customer_filename, blank=True)
    notes = models.TextField(blank=True, null=True)
    #-- Relation Many to Many with Users
    users = models.ManyToManyField(base.AUTH_USER_MODEL)
    
    class Meta:
        ordering = ['name']
        db_table = 'customers'
                                   
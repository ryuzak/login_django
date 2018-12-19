# -*- encoding: utf-8 -*-
from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import Group
#-- Models
from .models import Customer
from accounts.models import User
#-- Functions
import base_project.functions as func

#-- Import utilies
import base_project.utilies as ut


class CustomerForm(ModelForm):
	name = forms.CharField(
		label='Nombre',
		min_length=3,
		widget = forms.TextInput(
			attrs = {
				'class':'form-control'
			}
		)
	)

	website = forms.CharField(
		label = 'Sitio web',
		min_length = 3,
		required = False,
		widget = forms.TextInput(
			attrs = {
				'class':'form-control'
			}
		)
	)

	phone = forms.CharField(
		label = 'Telefono',
		min_length = 3,
		widget = forms.TextInput(
			attrs = {
				'class':'form-control'
			}
		)
	)

	street = forms.CharField(
		label = 'Calle',
		min_length = 3,
		required = False,
		widget = forms.TextInput(
			attrs = {
				'class':'form-control'
			}
		)
	)

	nostreet = forms.IntegerField(
		label='# de calle',
		required = False,
		widget = forms.NumberInput(
			attrs = {
				'class':'form-control'
			}
		)
	)

	colony = forms.CharField(
		label = 'Colonia',
		min_length=3,
		required = False,
		widget=forms.TextInput(
			attrs={
				'class':'form-control'
			}
		)
	)

	zipcode = forms.IntegerField(
		label = 'Codigo postal',
		required = False,
		widget = forms.NumberInput(
			attrs = {
				'class':'form-control'
			}
		)
	)

	email = forms.CharField(
		label = 'Email',
		min_length=3,
		widget=forms.TextInput(
			attrs={
				'class':'form-control'
			}
		)
	)

	country = forms.CharField(
		label = 'Pais',
		min_length = 1,
		widget = forms.Select(
			choices = ut.COUNTRYTYPES_CHOICES,
			attrs = {
				'class':'form-control'
			}
		)
	)


	class Meta:
		model = Customer
		fields = ('name', 'website', 'phone', 'email', 'street', 'nostreet', 'colony', 'zipcode', 'country', )


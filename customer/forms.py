# -*- coding: utf-8 -*-
"""
Created on Thu Oct  1 21:59:29 2020

@author: Abinesh
"""

from django import forms
from .models import Customer, IdentificationType, RelationshipType #, #AddressType,  
from masterdata.models import Client
from django.forms import DateInput
from datetime import date
from django.core.validators import RegexValidator
import re

re_alpha = re.compile('[^\W\d_]+$', re.UNICODE)
# alpha = RegexValidator(re_alpha, 'Only Alphabetic')
alpha = RegexValidator(r'^[a-zA-Z]*$', 'Only Alphabetic')

class CustomerForm(forms.Form):
    
    client_id = forms.ModelChoiceField(queryset=Client.objects.all(), 
                                       initial={'client_id': Client.pk},
                                       widget=forms.Select(
                                          attrs={ 'class': 'form-select' } ))
    customer_id = forms.CharField( max_length=12, required=False, 
                                   widget=forms.TextInput( 
                                          attrs={ "class": "form-control", 
                                                  "readonly": "readonly" } ),)
    external_id = forms.CharField( max_length=12, required=False,
                                   widget=forms.TextInput( 
                                          attrs={ "class": "form-control" } ),)
    title = forms.ChoiceField(choices=Customer.TITLE_LIST, 
                                   widget=forms.Select(
                                          attrs={ 'class': 'form-select' } ))
    first_name = forms.CharField( max_length=80,
                                   widget=forms.TextInput( 
                                          attrs={ "class": "form-control", } ),)
    middle_name = forms.CharField( max_length=80, required=False,
                                   widget=forms.TextInput( 
                                          attrs={ "class": "form-control"} ),)
    last_name = forms.CharField( max_length=80, 
                                      widget=forms.TextInput( 
                                          attrs={ "class": "form-control" } ),)
    name_at_birth = forms.CharField( max_length=80, required=False,
                                      widget=forms.TextInput( 
                                          attrs={ "class": "form-control" } ),)
    full_name = forms.CharField( max_length=160, required=False,
                                      widget=forms.TextInput( 
                                          attrs={ "class": "form-control" } ),)
    nick_name = forms.CharField( max_length=80, required=False, 
                                      widget=forms.TextInput( 
                                          attrs={ "class": "form-control" } ),)
    gender = forms.ChoiceField(choices=Customer.GENDER_LIST, 
                                      widget=forms.Select(
                                          attrs={ 'class': 'form-select' } ))
    birth_place = forms.CharField( max_length=80, 
                                      widget=forms.TextInput( 
                                          attrs={ "class": "form-control" } ),)    
    marital_status = forms.ChoiceField(choices=Customer.MARITAL_LIST, 
                                      widget=forms.Select(
                                          attrs={ 'class': 'form-select' } ))
    occupation = forms.CharField( max_length=80, 
                                      widget=forms.TextInput( 
                                          attrs={ "class": "form-control" } ),)
    nationality = forms.CharField( max_length=80, 
                                      widget=forms.TextInput( 
                                          attrs={ "class": "form-control" } ),)
    date_of_birth = forms.DateField( widget = DateInput(attrs={'type': 'date'}) )
    date_of_marriage = forms.DateField( required=False, 
                                        widget = DateInput(attrs={'type': 'date'}) )
    date_of_death = forms.DateField( required=False, 
                                     widget = DateInput(attrs={'type': 'date'}) )
    valid_from = forms.DateField( widget = DateInput(attrs={'type': 'date'}),
                                  initial=date.today())
    valid_to = forms.DateField( widget = DateInput(attrs={'type': 'date',
                                                           "readonly": "readonly" }),
                               initial=date(9999,12,31))
    status = forms.ChoiceField(choices=Customer.STATUS_LIST, 
                                      widget=forms.Select(
                                          attrs={ "class": "form-select", 
                                                 "readonly": "readonly" } ),
                                      initial='A')
    
    id_type = forms.ModelChoiceField(queryset=IdentificationType.objects.all(), 
                                       initial={'id_type': IdentificationType.pk},
                                       widget=forms.Select(
                                          attrs={ 'class': 'form-select' } ))
    id_number = forms.CharField( max_length=80, 
                                      widget=forms.TextInput( 
                                          attrs={ "class": "form-control" } ),)
    
    perm_house = forms.CharField( max_length=20, 
                                      widget=forms.TextInput( 
                                          attrs={ "class": "form-control" } ),)
    perm_building = forms.CharField( max_length=80, required=False,
                                      widget=forms.TextInput( 
                                          attrs={ "class": "form-control" } ),)
    perm_street_1 = forms.CharField( max_length=80, 
                                      widget=forms.TextInput( 
                                          attrs={ "class": "form-control" } ),)
    perm_street_2 = forms.CharField( max_length=80, required=False,
                                      widget=forms.TextInput( 
                                          attrs={ "class": "form-control" } ),)
    perm_village = forms.CharField( max_length=80, required=False,
                                      widget=forms.TextInput( 
                                          attrs={ "class": "form-control" } ),)
    perm_taluk = forms.CharField( max_length=80, required=False,
                                      widget=forms.TextInput( 
                                          attrs={ "class": "form-control" } ),)
    perm_district = forms.CharField( max_length=80, required=False,
                                      widget=forms.TextInput( 
                                          attrs={ "class": "form-control" } ),)
    perm_city = forms.CharField( max_length=40, 
                                      widget=forms.TextInput( 
                                          attrs={ "class": "form-control" } ),)
    perm_postal_code = forms.CharField( max_length=20, 
                                      widget=forms.TextInput( 
                                          attrs={ "class": "form-control" } ),)
    perm_region = forms.CharField( max_length=40, 
                                      widget=forms.TextInput( 
                                          attrs={ "class": "form-control" } ),)
    perm_country = forms.CharField( max_length=40, 
                                      widget=forms.TextInput( 
                                          attrs={ "class": "form-control" } ),)
    
    cont_house = forms.CharField( max_length=20, 
                                      widget=forms.TextInput( 
                                          attrs={ "class": "form-control" } ),)
    cont_building = forms.CharField( max_length=80, required=False,
                                      widget=forms.TextInput( 
                                          attrs={ "class": "form-control" } ),)
    cont_street_1 = forms.CharField( max_length=80, 
                                      widget=forms.TextInput( 
                                          attrs={ "class": "form-control" } ),)
    cont_street_2 = forms.CharField( max_length=80, required=False,
                                      widget=forms.TextInput( 
                                          attrs={ "class": "form-control" } ),)
    cont_village = forms.CharField( max_length=80, required=False,
                                      widget=forms.TextInput( 
                                          attrs={ "class": "form-control" } ),)
    cont_taluk = forms.CharField( max_length=80, required=False,
                                      widget=forms.TextInput( 
                                          attrs={ "class": "form-control" } ),)
    cont_district = forms.CharField( max_length=80, required=False,
                                      widget=forms.TextInput( 
                                          attrs={ "class": "form-control" } ),)
    cont_city = forms.CharField( max_length=40, 
                                      widget=forms.TextInput( 
                                          attrs={ "class": "form-control" } ),)
    cont_postal_code = forms.CharField( max_length=20, 
                                      widget=forms.TextInput( 
                                          attrs={ "class": "form-control" } ),)
    cont_region = forms.CharField( max_length=40, 
                                      widget=forms.TextInput( 
                                          attrs={ "class": "form-control" } ),)
    cont_country = forms.CharField( max_length=40, 
                                      widget=forms.TextInput( 
                                          attrs={ "class": "form-control" } ),)
    
    telephone = forms.CharField( max_length=15, required=False,
                                      widget=forms.TextInput( 
                                          attrs={ "class": "form-control" } ),)
    mobile_phone = forms.CharField( max_length=15, 
                                      widget=forms.TextInput( 
                                          attrs={ "class": "form-control" } ),)
    alternate_contact = forms.CharField( max_length=15, 
                                      widget=forms.TextInput( 
                                          attrs={ "class": "form-control" } ),)
    email_id = forms.CharField( max_length=80, required=False,
                                      widget=forms.TextInput( 
                                          attrs={ "class": "form-control" } ),) 
    
    rel_type = forms.ModelChoiceField(queryset=RelationshipType.objects.all(), 
                                       initial={'rel_type': RelationshipType.pk},
                                       widget=forms.Select(
                                          attrs={ 'class': 'form-select' } )) 
    rel_title = forms.ChoiceField(choices=Customer.TITLE_LIST, 
                                   widget=forms.Select(
                                          attrs={ 'class': 'form-select' } ))
    rel_first_name = forms.CharField( max_length=80,
                                   widget=forms.TextInput( 
                                          attrs={ "class": "form-control", } ),)
    rel_middle_name = forms.CharField( max_length=80, required=False,
                                   widget=forms.TextInput( 
                                          attrs={ "class": "form-control"} ),)
    rel_last_name = forms.CharField( max_length=80, 
                                      widget=forms.TextInput( 
                                          attrs={ "class": "form-control" } ),)
    rel_full_name = forms.CharField( max_length=160, required=False,
                                      widget=forms.TextInput( 
                                          attrs={ "class": "form-control" } ),)
    rel_mobile = forms.CharField( max_length=15, 
                                      widget=forms.TextInput( 
                                          attrs={ "class": "form-control" } ),)
    
# class AddressForm(forms.Form):    
# ## Customer Address
#     address_type = forms.ModelChoiceField(queryset=AddressType.objects.all(), 
#                                        initial={'address_type': AddressType.pk},
#                                        widget=forms.Select(
#                                           attrs={ 'class': 'form-select' } )) 
#     unit_number = forms.CharField( max_length=20, 
#                                       widget=forms.TextInput( 
#                                           attrs={ "class": "form-control" } ),)
#     building = forms.CharField( max_length=80, required=False,
#                                       widget=forms.TextInput( 
#                                           attrs={ "class": "form-control" } ),)
#     street_1 = forms.CharField( max_length=80, 
#                                       widget=forms.TextInput( 
#                                           attrs={ "class": "form-control" } ),)
#     street_2 = forms.CharField( max_length=80, required=False,
#                                       widget=forms.TextInput( 
#                                           attrs={ "class": "form-control" } ),)
#     street_3 = forms.CharField( max_length=80, required=False,
#                                       widget=forms.TextInput( 
#                                           attrs={ "class": "form-control" } ),)
#     street_4 = forms.CharField( max_length=80, required=False,
#                                       widget=forms.TextInput( 
#                                           attrs={ "class": "form-control" } ),)
#     street_5 = forms.CharField( max_length=80, required=False,
#                                       widget=forms.TextInput( 
#                                           attrs={ "class": "form-control" } ),)
#     city = forms.CharField( max_length=40, 
#                                       widget=forms.TextInput( 
#                                           attrs={ "class": "form-control" } ),)
#     postal_code = forms.CharField( max_length=20, 
#                                       widget=forms.TextInput( 
#                                           attrs={ "class": "form-control" } ),)
#     region = forms.CharField( max_length=40, 
#                                       widget=forms.TextInput( 
#                                           attrs={ "class": "form-control" } ),)
#     country = forms.CharField( max_length=40, 
#                                       widget=forms.TextInput( 
#                                           attrs={ "class": "form-control" } ),)
#     telephone = forms.CharField( max_length=15, required=False,
#                                       widget=forms.TextInput( 
#                                           attrs={ "class": "form-control" } ),)
#     mobile_phone = forms.CharField( max_length=15, 
#                                       widget=forms.TextInput( 
#                                           attrs={ "class": "form-control" } ),)
#     alternate_contact = forms.CharField( max_length=15, 
#                                       widget=forms.TextInput( 
#                                           attrs={ "class": "form-control" } ),)
#     email_id = forms.CharField( max_length=80, required=False,
#                                       widget=forms.TextInput( 
#                                           attrs={ "class": "form-control" } ),)
# # =============================================================================
# # ## Customer Identification
# #     id_type = forms.ModelChoiceField(queryset=IdentificationType.objects.all(), 
# #                                        initial={'id_type': IdentificationType.pk},
# #                                        widget=forms.Select(
# #                                           attrs={ 'class': 'form-select' } ))
# #     id_number = forms.CharField( max_length=80, 
# #                                       widget=forms.TextInput( 
# #                                           attrs={ "class": "form-control" } ),)
# # =============================================================================

# class IDForm(forms.Form):
# ## Customer Identification
#     id_type = forms.ModelChoiceField(queryset=IdentificationType.objects.all(), 
#                                        initial={'id_type': IdentificationType.pk},
#                                        widget=forms.Select(
#                                           attrs={ 'class': 'form-select' } ))
#     id_number = forms.CharField( max_length=80, 
#                                       widget=forms.TextInput( 
#                                           attrs={ "class": "form-control" } ),)
class CustSearchForm(forms.Form):
    customer_id = forms.CharField( max_length=12, required=False, widget=forms.TextInput( 
                                    attrs={ "class": "form-control" } ),)
    first_name = forms.CharField( max_length=80, required=False,
                                   widget=forms.TextInput( 
                                          attrs={ "class": "form-control", } ),)
    last_name = forms.CharField( max_length=80, required=False,
                                      widget=forms.TextInput( 
                                          attrs={ "class": "form-control" } ),)
    full_name = forms.CharField( max_length=160, required=False,
                                      widget=forms.TextInput( 
                                          attrs={ "class": "form-control" } ),)
    gender = forms.ChoiceField(choices=Customer.GENDER_LIST,  
                                      widget=forms.Select(
                                          attrs={ 'class': 'form-select' } ))
    village = forms.CharField( max_length=80, required=False,
                                      widget=forms.TextInput( 
                                          attrs={ "class": "form-control" } ),)
    taluk    = forms.CharField( max_length=80, required=False,
                                      widget=forms.TextInput( 
                                          attrs={ "class": "form-control" } ),)
    district = forms.CharField( max_length=80, required=False,
                                       widget=forms.TextInput( 
                                           attrs={ "class": "form-control" } ),)                                  
    city = forms.CharField( max_length=40,  required=False,
                                      widget=forms.TextInput( 
                                          attrs={ "class": "form-control" } ),)
    postal_code = forms.CharField( max_length=20,  required=False,
                                      widget=forms.TextInput( 
                                          attrs={ "class": "form-control" } ),)
    region = forms.CharField( max_length=40,  required=False,
                                      widget=forms.TextInput( 
                                          attrs={ "class": "form-control" } ),)
    id_number = forms.CharField( max_length=80,  required=False,
                                      widget=forms.TextInput( 
                                          attrs={ "class": "form-control" } ),)

class CustManageForm(forms.Form):
    customer_id = forms.CharField( max_length=12, required=False, widget=forms.TextInput( 
                                    attrs={ "class": "form-control" } ),)
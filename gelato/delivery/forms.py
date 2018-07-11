# -*- coding: utf-8 -*-
from django import forms
from django.forms import TextInput, EmailInput, ModelForm
from .models import IceCream, User, Delivery



class IceCreamForm(ModelForm):
    class Meta:
        model = IceCream
        fields = '__all__'


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = '__all__'


class DeliveryForm(ModelForm):

    class Meta:
        model = Delivery
        fields = ["user"]


class Delivery_select_iceCreamForm(forms.Form):
        barcode = forms.CharField(
            widget=forms.TextInput(attrs={'autofocus': 'autofocus',
                                          'label' : 'code barre',
                                          'max_length' : 20,
                                          'required' : 'true',
                                          'placeholder' : 'code barre'}))



class Delivery_quantity_iceCreamForm(forms.Form):
    quantity = forms.IntegerField(label='quantité',min_value=0)






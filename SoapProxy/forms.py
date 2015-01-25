# -*- coding: utf-8 -*-
from django import forms
from splitjson.widgets import SplitJSONWidget
from . import models


class ProxyServiceForm(forms.ModelForm):
    #methods = forms.CharField(max_length=255 ,widget= forms.TextInput(attrs={'type':'text', 'class' : 'form-control', 'readonly':True}))
    attrs = {'class': 'special', 'size': '40'}
    methods = forms.CharField(widget=SplitJSONWidget(attrs=attrs, debug=False))
    #methods = forms.CharField(widget=SplitJSONWidget(attrs={'type':'text', 'class' : 'form-control'}, debug=False))
    wsdl = forms.URLField(widget= forms.TextInput(attrs={'type':'text', 'class' : 'form-control'}))
    slug = forms.CharField(widget= forms.TextInput(attrs={'type':'text', 'class' : 'form-control', 'readonly':True}))
    name = forms.CharField(widget= forms.TextInput(attrs={'type':'text', 'class' : 'form-control'}))
    #category = forms.ModelChoiceField(widget=forms.ModelChoiceField(attrs={'class' : 'form-control',}))




    class Meta:
        model = models.ProxyService
        fields = ['category','wsdl','name','slug','methods']


class ProxyTransactionServiceForm(forms.ModelForm):
    #method = forms.CharField(max_length=255 ,widget= forms.TextInput(attrs={'type':'text', 'class' : 'form-control', 'readonly':True}))
    data = forms.CharField(widget=SplitJSONWidget(attrs={'type':'text', 'class' : 'form-control',}, debug=False))
    #wsdl = forms.URLField(widget= forms.TextInput(attrs={'type':'text', 'class' : 'form-control'}))
    #slug = forms.CharField(widget= forms.TextInput(attrs={'type':'text', 'class' : 'form-control', 'readonly':True}))
    #name = forms.CharField(widget= forms.TextInput(attrs={'type':'text', 'class' : 'form-control'}))
    #proxyService = forms.ModelChoiceField(widget=forms.ModelChoiceField(attrs={'class' : 'form-control',}))




    class Meta:
        model = models.ProxyServiceTransactions
        fields = ['proxyService','data',]






class catgeoryForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    slug = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'readonly':True}))

    class Meta:
        #fields =('name','slug')
        model = models.Category




class WsdlForm(forms.Form):
    wsdl = forms.URLField(label="Please Enter URL of wsdl FILE", widget=forms.TextInput(attrs = {'type':'text', 'class' : 'form-control'}))
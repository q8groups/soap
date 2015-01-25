# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic import ListView,edit
from django.core.urlresolvers import reverse_lazy
from django.contrib.messages import views as messageviews
from braces import views as bracesViews

from SoapProxy import models
from .  import  forms
from .utils import SoapClient,recursive_asdict


import json



# Create your views here.
class SetCategoryMixin(object):
    """
    Mixin allows you to set a static headline through a static property on the
    class or programmatically by overloading the get_headline method.
    """

    def get_context_data(self, **kwargs):
        kwargs = super(SetCategoryMixin, self).get_context_data(**kwargs)
        # Update the existing context dict with the provided headline.
        kwargs.update({"category": models.Category.objects.all()})
        return kwargs

class CategoryList(SetCategoryMixin,bracesViews.SetHeadlineMixin,ListView):
    model = models.Category
    template_name = "SoapProxy/list_category.html"
    paginate_by = 2
    headline = "Category List"



class CategoryCreate(SetCategoryMixin,messageviews.SuccessMessageMixin,edit.CreateView):
    template_name = "SoapProxy/add.html"
    model = models.Category
    form_class = forms.catgeoryForm
    success_url = reverse_lazy('category_list')
    success_message = "Success"
    headline = "List Category"



class CategoryCreate(SetCategoryMixin,messageviews.SuccessMessageMixin,edit.CreateView):
    template_name = "SoapProxy/add.html"
    model = models.ProxyServiceTransactions
    form_class = forms.catgeoryForm
    success_url = reverse_lazy('category_list')
    success_message = "Success"
    headline = "List Category"



class ServiceList(SetCategoryMixin,bracesViews.SetHeadlineMixin,ListView):
    model = models.ProxyService
    template_name = "SoapProxy/list_service.html"
    paginate_by = 20
    headline = "List Services"



class ServiceCreate(SetCategoryMixin,messageviews.SuccessMessageMixin,edit.CreateView):
    template_name = "SoapProxy/add_service.html"
    model = models.Category
    form_class = forms.ProxyServiceForm
    success_url = reverse_lazy('service_list')
    success_message = "Success"





def WSDLFile(request):
    form = forms.WsdlForm(request.POST or None)
    if form.is_valid():
        return GenericeSoapView(request=request)
    template = 'add.html'
    context = RequestContext(request, {'form': form,})
    return render_to_response(template, context)






def GenericeSoapView(request):
    client = SoapClient(wsdl=request.POST.get('wsdl'))
    out = client.GetMethods()[0]
    form = forms.ProxyServiceForm(initial={'params': json.dumps(out['inputs']), 'method': out['method'], 'wsdl':request.POST.get('wsdl') })
    template = 'base3.html'
    context = RequestContext(request, {'form': form})
    return render_to_response(template, context)


def SoapRequest(request):
    obj = models.ProxyService.objects.all()[0]
    obj.methods = json.loads(obj.methods)
    req = None
    res = None

    if request.POST:
        form = forms.ProxyServiceForm(request.POST)
    else:
        form = forms.ProxyServiceForm(instance=obj)
    if form.is_valid():
        myDict = json.loads(form.cleaned_data['methods'])
        for k in myDict:
            cli = SoapClient(wsdl=obj.wsdl)
            cli.call(name=k,params=myDict[k])
            req = str(cli.client.last_sent())
            res = str(cli.client.last_received())
            import xml.dom.minidom
            req = xml.dom.minidom.parseString(req).toprettyxml()
            print req

    template = 'SoapProxy/add_service.html'
    context = RequestContext(request, {'form': form,'req':req,'res':res})
    return render_to_response(template, context)



def GenericSoapViewResponse(request):
    form = forms.ProxyServiceForm(request.POST)
    if form.is_valid():
        # validate and save
        myparams = json.loads(form.cleaned_data['params'])
        client = SoapClient(wsdl=request.POST.get('wsdl'))
        responsexml = client.call(name=form.cleaned_data['method'],params=myparams)
    else:
        responsexml = ''

    template = 'base3.html'
    context = RequestContext(request, {'form': form,'responsexml':responsexml})
    return render_to_response(template, context)





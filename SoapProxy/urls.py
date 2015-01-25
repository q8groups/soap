from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns('',
                       url(r'^category/list/$', views.CategoryList.as_view(), name='category_list'),
  url(r'^category/new/$', views.CategoryCreate.as_view(), name='category_new'),
                        url(r'^service/list/$', views.ServiceList.as_view(), name='service_list'),
  url(r'^service/new/$', views.ServiceCreate.as_view(), name='service_new'),
    url(r'^wsdls/$', views.WSDLFile,name='wsdlview'),
    url(r'^services/$', views.SoapRequest, name='soapview'),
     url(r'^services/response/$', views.GenericeSoapView, name='soapresponse'),

)
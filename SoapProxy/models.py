from django.db import models
import json
import traceback
import sys
from jsonfield import JSONField
from .utils import SoapClient,recursive_asdict
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    def __unicode__(self):
        return self.name

class Methods(models.Model):
    name = models.CharField(max_length=255,verbose_name="Name")
    params = models.TextField()
    def __unicode__(self):
        return self.name+' '+str(self.params)

class ProxyService(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    wsdl = models.URLField()
    endpoint = models.URLField(blank=True)
    category = models.ForeignKey(Category)
    methods = JSONField(blank=True)









    def soap(self):
        try:
            self.client =  SoapClient(wsdl=self.wsdl)
            return self.client.GetMethods()
        except Exception, err:
            self.client=None
            print traceback.format_exc()
            return ""



    def response(self,name,params):
        if self.client:
            try:
                return self.client.call(name=name,params=params)
            except:
                pass
            return None








    def __unicode__(self):
        return self.name





class ProxyServiceTransactions(models.Model):
    proxyService = models.ForeignKey(ProxyService)
    proxyMethod = models.ForeignKey(Methods)
    data = JSONField()


from django.db.models.signals import pre_save, pre_delete, m2m_changed

def handle_flow(sender, instance, *args, **kwargs):
     instance.methods = instance.soap()
     #print("Signal catched !")

pre_save.connect(handle_flow, sender=ProxyService)

import logging
from suds.sax.element import Element
from suds.client import Client
from suds.sudsobject import asdict

logging.basicConfig(level=logging.INFO)
logging.getLogger('suds.client').setLevel(logging.DEBUG)
import json


def recursive_asdict(d):
        """Convert Suds object into serializable format."""
        out = {}
        for k, v in asdict(d).iteritems():
            if hasattr(v, '__keylist__'):
                out[k] = recursive_asdict(v)
            elif isinstance(v, list):
                out[k] = []
                for item in v:
                    if hasattr(item, '__keylist__'):
                        out[k].append(recursive_asdict(item))
                    else:
                        out[k].append(item)
            else:
                out[k] = v
        return out

class SoapClient:
    def __init__(self,wsdl,username='extdealers',password='extdealers123'):
        self.client = Client(wsdl)
        self.username = username
        self.password = password
        #self.client.set_options(soapheaders=self.GenerateSoapHeader())
        self.GenerateMethods()



    def GenerateMethods(self):
        methodInputDict = {}
        for method in self.client.wsdl.services[0].ports[0].methods.values():
            for part in method.soap.input.body.parts:
                methodInputDict[str(method.name)]={}
                for k,v in self.client.factory.create(part.element[0]):
                    methodInputDict[str(method.name)][k]=v
        self.methods =  json.dumps(methodInputDict)





    def GenerateSoapHeader(self):
        wataniyaAuth = ('wataniya', 'http://osb.wataniya.com')
        token = Element('auth', ns=wataniyaAuth)
        username = Element('username').setText(self.username)
        password = Element('password').setText(self.password)
        token.append(username)
        token.append(password)
        return token


    def ToJson(self):
        return json.dumps(self.methods)
    def GetMethods(self):
        return self.methods



    def call(self,name,params):
        return (getattr(self.client.service,name)(**params))






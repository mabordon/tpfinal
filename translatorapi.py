import requests
import json
from itbatools import get_api_translator_property_hook
from singleton import Singleton
class TranslatorApi(metaclass=Singleton):
      def __init__(self):
             self._propertyhook=get_api_translator_property_hook()
      def translate(self,texto):
                  response = requests.request("GET", self._propertyhook.url,                                                    
                                                   params={"lang":self._propertyhook.language,
                                                           "key":self._propertyhook.key,
                                                           "text":texto })
                  
                  return response   
      @classmethod
      def get_instance(cls):
            return TranslatorApi()

if __name__=='__main__':
         t=TranslatorApi.get_instance()
         mensaje="{'Pros': 'Un lugar donde se piensa en la gente. Más allá de beneficios o grandes salarios. Lo que importa es la gente y su desarrollo.', 'Cons': 'Podrían mejorar el rango salarial, pero en general está bien'}"
         resultado=t.translate(mensaje)
         mensaje=json.loads(resultado.text)
         print(mensaje["text"][0])
      
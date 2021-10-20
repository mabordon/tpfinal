import json
import sys
import logging
import os.path
from singleton import Service

services={"api_translator":"apitranslatorconfig.json","comentarios_db":"dbconfig.json","firefox":"firefox.json"}

class PropertyHook(metaclass=Service):        
             def __init__(self,type): 
                         self.type=type                         
             def __load_properties(self,inifile):                
                  with open(inifile,'r') as file:                                     
                       self.__dict__=dict((json.load(file)).items())       
             @classmethod                
             def get_instance(cls,servicetype):
                       _instance=None         
                       if servicetype in services:            
                              _instance=PropertyHook(servicetype)
                              _instance.__load_properties(services[servicetype])
                       return _instance
             
               

def get_db_property_hook():
         return PropertyHook.get_instance("comentarios_db")

def get_api_translator_property_hook():
        return PropertyHook.get_instance("api_translator")

def get_firefox_driver_hook():
         return PropertyHook.get_instance("firefox")

def get_itba_logger(logname,screen=False):    
          
          def find_handler(handlername,isfile=False): 
              if isfile:
                 items=list(filter(lambda x:os.path.basename(x.stream.name)==handlername,l.handlers))                 
              else:
                 items=list(filter(lambda x:x.stream.name==handlername,l.handlers))
              
              return len(items)>0                
             
          logging.basicConfig(level=logging.DEBUG,handlers=[])
          l= logging.getLogger(logname)    
          formatter=logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')         
          
          if not find_handler("{0}.log".format(logname),isfile=True): 
              
              file_handler = logging.FileHandler(filename="logs/{0}.log".format(logname))
              file_handler.setFormatter(formatter)            
              l.handlers.append(file_handler)  
              
          if screen and not find_handler("<stdout>"):

               stdout_handler = logging.StreamHandler(sys.stdout)
               stdout_handler.setFormatter(formatter)  
               l.handlers.append(stdout_handler)                  
   
          return logging.getLogger(logname)   
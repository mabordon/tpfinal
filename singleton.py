class Singleton(type):
               __cls__={}
               def __call__(cls,*args,**kwargs):                  
                                                  
                          if cls not in Singleton.__cls__:
                                       Singleton.__cls__[cls]=type.__call__(cls,*args,**kwargs)
                          return Singleton.__cls__[cls]

class Service(type):
               __cls__={}
               def __call__(cls,*args,**kwargs):                     
                          service_type="{0}_{1}".format(cls.__name__,args[0])                         
                          if service_type not in Service.__cls__:
                                       Service.__cls__[service_type]=type.__call__(cls,*args,**kwargs)
                          return Service.__cls__[service_type]
import requests
from itertools import cycle
from proxyscraper import ProxyScraper
from singleton import Singleton

class ProxyPool(metaclass=Singleton):
      def __init__(self):
               self.proxyscraper=ProxyScraper.get_instance()
               self.proxies_pool=cycle(self.proxyscraper.get_proxy_list())
      def get_next(self):
                available_proxy=next(self.proxies_pool)
                return available_proxy
      def refresh(self):
            self.proxies_pool=cycle(self.proxyscraper.refresh_server_list())
      @classmethod
      def get_instance(cls):
            return ProxyPool()
 

    
if __name__=='__main__':
         _instance=ProxyPool()
         proxy=_instance.get_instance().get_next()
         print(proxy)
import requests
from itertools import cycle
from singleton import Singleton
from lxml.html import fromstring

class ProxyScraper(metaclass=Singleton):
             def __init__(self):
                    self.url = 'https://free-proxy-list.net/' 
                    self.proxies=[]
             def refresh_server_list(self):                    
                    self.proxies=self.start_scraping()  
                    return self.proxies                 
             def start_scraping(self):
                    response = requests.get(self.url)
                    parser = fromstring(response.text)              
                    proxies =[]
                    for attribute in parser.xpath('//tbody/tr'):
                        if (attribute.xpath('.//td[7][contains(text(),"yes")]')): 
                            proxy = ":".join([attribute.xpath('.//td[1]/text()')[0], attribute.xpath('.//td[2]/text()')[0]])
                            proxies.append(proxy) 
                              
                    return proxies

             @classmethod
             def get_instance(cls):
                return ProxyScraper()
             def get_proxy_list(self):
                    self.refresh_server_list()
                    return self.proxies
if  __name__=='__main__':
       _instance=ProxyScraper.get_instance()
       print(_instance.get_proxy_list())
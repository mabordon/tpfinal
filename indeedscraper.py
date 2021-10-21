from selenium import webdriver 
import time
from selenium.webdriver.firefox.options import Options
opts = Options()
opts.headless = True
assert opts.headless
from itbatools import get_firefox_driver_hook
from singleton import Singleton
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.proxy import Proxy, ProxyType
from proxyservice import ProxyPool

__website__="ar.indeed.com"
__url__="https://{0}/cmp/Everis/reviews?fcountry=ALL".format(__website__)
__sleeptime__=2
__max_score__=5
class IndeedScraper(metaclass=Singleton):
      def __init__(self,proxy):
             self.driver=webdriver.Firefox(executable_path= get_firefox_driver_hook().executable_path,options=opts, proxy=proxy) 
             self.baseurl =__url__   
             self.driver.get(self.baseurl)     
            
      @classmethod
      def get_instance(cls,proxy):
            return IndeedScraper(proxy)
      def get_rating_summary(self):                  
           company_ratings={}
           company_ratings["website"]=__website__
           company_ratings["maxscore"]=__max_score__            
                   #Recuperamos los puntajes del sitio 
           sections=self.driver.find_elements_by_class_name("css-mcjliz")
           for section in sections:
                tags=section.find_elements_by_tag_name("span")             
                aspect=tags[2].text
                rating=tags[0].text
                company_ratings[aspect]=rating    
           return company_ratings     
      def get_comments(self):    
             comments=[]  


if __name__=='__main__':
        pool = ProxyPool.get_instance()
        pool.refresh()        
        myProxy = pool.get_next()
        proxy = Proxy({
                 'proxyType': ProxyType.MANUAL,
                 'httpProxy': myProxy,
                 'ftpProxy': myProxy,
                 'sslProxy': myProxy,
                 'noProxy': '' 
                 })
        instance=IndeedScraper.get_instance(proxy)
        print(instance.get_rating_summary())
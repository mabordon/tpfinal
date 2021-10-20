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
__url__="https://openqube.io/company/everis/"
__sleeptime__=2
__counter__=16
class OpenQubeScraper(metaclass=Singleton):
      def __init__(self,proxy):
             self.driver=driver = webdriver.Firefox(executable_path= get_firefox_driver_hook().executable_path,options=opts, proxy=proxy) 
             self.baseurl =__url__
      @classmethod
      def get_instance(cls,proxy):
            return OpenQubeScraper(proxy)
      def get_comments(self):    
             comments=[]  
             self.driver.get(self.baseurl) 
             lista= self.driver.find_elements_by_class_name("reviewlist__items")
             counter=self.driver.find_elements_by_class_name("reviewlist__title")
             for scroll_index in range(0,__counter__):
                    button=self.driver.find_element_by_class_name("viewmore__button")   
                    time.sleep(__sleeptime__)            
                    self.driver.execute_script("arguments[0].click();", button)
             articles= self.driver.find_elements_by_class_name("review")
             for article in articles:                    
                     textos= article.find_elements_by_class_name("review__text") 
                     for texto in textos:
                        procons=texto.find_element_by_tag_name("strong")
                        item= texto.find_element_by_tag_name("span") 
                        if len(item.text)>0:     
                           print(procons.text,item.text)
                           comments.append({procons.text:item.text})
             return comments
                    

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
        instance=OpenQubeScraper.get_instance(proxy)
        for items in instance.get_comments():
            print(items)
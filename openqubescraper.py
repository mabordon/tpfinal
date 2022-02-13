from selenium import webdriver 
import time
import json
from selenium.webdriver.firefox.options import Options
opts = Options()
opts.headless = True
assert opts.headless
from itbatools import get_firefox_driver_hook
from singleton import Singleton
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.proxy import Proxy, ProxyType
from proxyservice import ProxyPool
from itbatools import extract_digits
from translatorapi import TranslatorApi
from comentarioDB import ComentarioDB

__website__="openqube.io"
__url__="https://{0}/company/everis/".format(__website__)
__sleeptime__=2
__records__=2
__max_score__=10

translator=TranslatorApi.get_instance()   
dbComentarios=ComentarioDB.getDataBase()   

class OpenQubeScraper(metaclass=Singleton):
      def __init__(self,proxy):
             self.driver= webdriver.Firefox(executable_path= get_firefox_driver_hook().executable_path,options=opts, proxy=proxy) 
             self.baseurl =__url__
             self.driver.get(self.baseurl) 
      @classmethod
      def get_instance(cls,proxy):
            return OpenQubeScraper(proxy)
      def save_rating_summary(self):
          ratings={}        
          company_ratings=self.get_rating_summary() 
          rating_item=json.loads(translator.translate(json.dumps(company_ratings)).text)["text"][0]
          ratings["website"]="openqube.io" 
          ratings["rating"]=rating_item
          dbComentarios.insert_comentario(ratings)
      def get_rating_summary(self):
                         #Recuperar los puntajes del sitio                         
                         sections=self.driver.find_elements_by_class_name("company__item-rating")
                         company_ratings={}
                         company_ratings["website"]=__website__
                         company_ratings["maxscore"]=__max_score__
                         for section in sections:
                                  aspect=section.find_elements_by_class_name("company__item-ratingtxt")[0].text
                                  rating=section.find_elements_by_class_name("company__item-ratingnum")[0].text
                                  company_ratings[aspect]=rating
                         return company_ratings
      def add_comments(self):           
             lista= self.driver.find_elements_by_class_name("reviewlist__items")
             items=self.driver.find_elements_by_class_name("reviewlist__title")
             __counter__=(extract_digits(items[0].find_element_by_tag_name("span").text)//__records__)+1
             print(__counter__)
             for scroll_index in range(0,__counter__):
                    button=self.driver.find_element_by_class_name("viewmore__button")   
                    time.sleep(__sleeptime__)            
                    self.driver.execute_script("arguments[0].click();", button)
             articles= self.driver.find_elements_by_class_name("review")      
             for article in articles:                    
                     textos= article.find_elements_by_class_name("review__text") 
                     comment={}
                     for texto in textos:
                        procons=texto.find_element_by_tag_name("strong")
                        item= texto.find_element_by_tag_name("span") 
                        if len(item.text)>0:        
                           translated_comment=json.loads((translator.translate(item.text)).text)["text"][0]                      
                           comment[procons.text]= translated_comment 
                           comment["website"] =__website__                             
                     dbComentarios.insert_comentario(comment)        
                         

      def get_comments(self):    
             comments=[]           
             lista= self.driver.find_elements_by_class_name("reviewlist__items")
             items=self.driver.find_elements_by_class_name("reviewlist__title")
             __counter__=(extract_digits(items[0].find_element_by_tag_name("span").text)//__records__)+1
             print(__counter__)
             for scroll_index in range(0,__counter__):
                    button=self.driver.find_element_by_class_name("viewmore__button")   
                    time.sleep(__sleeptime__)            
                    self.driver.execute_script("arguments[0].click();", button)
             articles= self.driver.find_elements_by_class_name("review")
             for article in articles:                    
                     textos= article.find_elements_by_class_name("review__text") 
                     comment={}
                     for texto in textos:
                        procons=texto.find_element_by_tag_name("strong")
                        item= texto.find_element_by_tag_name("span") 
                        if len(item.text)>0:                       
                           comment[procons.text]=item.text
                     comments.append(comment)
             return comments
                    
def process_open_qub():
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
        print(instance.get_rating_summary())
        print("Borrando")
        dbComentarios.delete_many({"website":__website__})
        print("Fin borrado")
        instance.save_rating_summary()
        print("Guardando comentarios")
        instance.add_comments()


def print_comentarios():
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
       print(instance.get_rating_summary())
       print("Imprimiendo comentarios....")
       for items in instance.get_comments():
            print(items)     

if __name__=='__main__':
         print_comentarios()
   
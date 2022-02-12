from selenium import webdriver 
import time
import json
from selenium.webdriver.firefox.options import Options
opts = Options()
opts.headless = True
assert opts.headless
from itbatools import get_firefox_driver_hook,extract_digits
from singleton import Singleton
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.proxy import Proxy, ProxyType
from proxyservice import ProxyPool
from translatorapi import TranslatorApi
from comentarioDB import ComentarioDB

__website__="ar.indeed.com"
__url__="https://{0}/cmp/Ntt-Data/reviews?fcountry=ALL".format(__website__)
__sleeptime__=2
__max_score__=5
__page_size__=20

translator=TranslatorApi.get_instance()   
dbComentarios=ComentarioDB.getDataBase()   

class IndeedScraper(metaclass=Singleton):
      def __init__(self,proxy):
             self.driver=webdriver.Firefox(executable_path= get_firefox_driver_hook().executable_path,options=opts, proxy=proxy) 
             self.baseurl =__url__   
             self.driver.get(self.baseurl)     
            
      @classmethod
      def get_instance(cls,proxy):
            return IndeedScraper(proxy)
      def save_rating_summary(self):
          ratings={}        
          company_ratings=self.get_rating_summary() 
          rating_item=json.loads(translator.translate(json.dumps(company_ratings)).text)["text"][0]
          ratings["website"]=__website__
          ratings["rating"]=rating_item
          dbComentarios.insert_comentario(ratings)
      def get_rating_summary(self):                  
           company_ratings={}
           company_ratings["website"]=__website__
           company_ratings["maxscore"]=__max_score__            
                   #Recuperamos los puntajes del sitio 
           sections=self.driver.find_elements_by_class_name("css-mcjliz")
           print("Imprimiendo las secciones")
           for section in sections:
                print(section)
                tags=section.find_elements_by_tag_name("span")             
                aspect=tags[2].text
                rating=tags[0].text
                company_ratings[aspect]=rating    
           return company_ratings     

      def print_comments(self):             
                     reviews_counter=self.get_reviews_counter() 
                     counter=__page_size__
                     times=(reviews_counter //__page_size__)
                     print("La cantidad de iteraciones sera",times)         
                     for page in range(0,1):
                             self.add_comments() 
                             time.sleep(__sleeptime__)                              
                             url=self.baseurl+"&start={0}".format(counter)
                             print(url)
                             self.driver.get(url)
                             counter+=__page_size__
      
      def get_reviews_counter(self): 
          #Recupera la cantidad de reviews de la pagina        
          result=0
          div=self.driver.find_element_by_class_name("css-r5p2ca")
          if (div):
               result=extract_digits(div.find_element_by_tag_name("span").text)        
          return result        
      def add_comments(self):
            comments= self.driver.find_elements_by_class_name("css-e6s05i")
            page_comment={}
            for comment in comments:
                     item_title=comment.find_elements_by_class_name("css-i1omlj")
                     title=""   
                     if len(item_title)>0:
                              title=item_title[0].find_element_by_class_name("css-82l4gy").text 
                              page_comment["title"]=json.loads((translator.translate(title)).text)["text"][0]
                     item_body=comment.find_elements_by_class_name("css-rr5fiy")
                     if len(item_body)>0:
                           elem=item_body[0].find_elements_by_class_name("css-1cxc9zk")
                           page_comment["body"]=""
                           if len(elem)>0:                            
                                paragraphs=elem[0].find_elements_by_xpath("span/span")
                                for p in paragraphs:
                                    page_comment["body"]+=p.text
                           else:
                                 elem=item_body[0].find_elements_by_class_name("css-qodkr")
                                 if len(elem)>0:                            
                                       paragraphs=elem[0].find_elements_by_xpath("span/span")
                                       for p in paragraphs:
                                           page_comment["body"]+=p.text
                           page_comment["body"]=json.loads((translator.translate(page_comment["body"])).text)["text"][0]
                     if len(item_body)>1:                                 
                               procons_title=item_body[1].find_elements_by_tag_name("h2") 
                               div=item_body[1].find_elements_by_class_name("css-1z0411s")  

                               if (len(div)>0):
                                     pro=div[0].find_element_by_xpath("span/span").text   
                                     page_comment["Pros"]=pro

                               if (len(div)>1):                                      
                                    cons=div[1].find_element_by_xpath("span/span").text
                                    page_comment["Cons"]=cons
                               else:
                                    div=item_body[1].find_elements_by_class_name("css-1jysqrt")  
                                    if len(div)>0:
                                         pro=div[0].find_element_by_xpath("span/span").text
                                         page_comment["Pros"]=pro

                                    if (len(div)>1):                                       
                                        cons=div[1].find_element_by_xpath("span/span").text
                                        page_comment["Cons"]=cons                       
                               page_comment["website"] =__website__ 
                               page_comment["Pros"]=json.loads((translator.translate(page_comment["Pros"])).text)["text"][0]  
                               page_comment["Cons"]=json.loads((translator.translate(page_comment["Cons"])).text)["text"][0]
                               print(page_comment)            

def process_indeed():
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
        
      #  instance.save_rating_summary()
       # print("Fin del guardado")
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
        instance=IndeedScraper.get_instance(proxy)
        print(instance.get_rating_summary())
        print(instance.get_reviews_counter())
       # instance.add_comments()
        instance.print_comments()

if __name__=='__main__':
         print_comentarios()
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
     
      def save_ratings_summary(self):    
                titles=self.driver.find_elements_by_class_name("css-7bbylr")   
                ratings=self.driver.find_elements_by_class_name("css-1vmx0e0")
                company_ratings={}
                for title, rating in zip(titles,ratings):
                     company_ratings[title.text]=rating.text
                company_ratings["website"]=__website__
                company_ratings["maxscore"]=__max_score__ 
                print(company_ratings) 
                dbComentarios.insert_comentario(company_ratings)

      def print_comments(self):             
                     reviews_counter=self.get_reviews_counter() 
                     counter=__page_size__
                     times=(reviews_counter //__page_size__)
                     print("La cantidad de iteraciones sera",times)         
                     for page in range(0,5):
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
            for comment in comments:
                     page_comment={}
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
                           if "body" in page_comment.keys():                
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
                               if "Pros" in page_comment.keys():
                                   page_comment["Pros"]=json.loads((translator.translate(page_comment["Pros"])).text)["text"][0] 

                               if "Cons" in page_comment.keys(): 
                                   page_comment["Cons"]=json.loads((translator.translate(page_comment["Cons"])).text)["text"][0]
                           
                               dbComentarios.insert_comentario(page_comment)  
                               
                             
                              

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
        instance.save_ratings_summary()
       # print(instance.get_reviews_counter())
        print("Borrando comentarios")
        dbComentarios.delete_many({"website":__website__})
        print("Fin borrando comentarios")
        instance.print_comments()


if __name__=='__main__':
         process_indeed()
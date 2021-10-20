from selenium import webdriver 
import time
from selenium.webdriver.firefox.options import Options
opts = Options()
opts.headless = True
assert opts.headless
from itbatools import get_firefox_driver_hook
from singleton import Singleton
from selenium.webdriver.support.ui import WebDriverWait

__url__="https://ar.indeed.com/cmp/Everis/reviews?fcountry=ALL"
__sleeptime__=2
class IndeedScraper(metaclass=Singleton):
      def __init__(self):
             self.driver=driver = webdriver.Firefox(executable_path= get_firefox_driver_hook().executable_path,options=opts) 
             self.baseurl =__url__
      @classmethod
      def get_instance(cls):
            return IndeedScraper()
      def get_comments(self):    
             comments=[]  



if __name__=='__main__':
        instance=IndeedScraper.get_instance()
        for items in instance.get_comments():
            print(items)
from selenium import webdriver 
from selenium.webdriver.firefox.options import Options
opts = Options()
opts.headless = True
assert opts.headless
from itbatools import get_firefox_driver_hook
#driver = webdriver.Firefox(executable_path= get_firefox_driver_hook().executable_path) #"C:\Users\Administrator\Downloads\geckodriver-v0.30.0-win64\geckodriver.exe")
driver = webdriver.Firefox(executable_path=r"C:\Users\Administrator\Downloads\geckodriver-v0.30.0-win64\geckodriver.exe",options =opts)
print(driver)
#driver.get('http://www.gutenberg.org/ebooks/search/%3Fsort_order%3Drelease_date')
driver = webdriver.Firefox(executable_path= get_firefox_driver_hook().executable_path) #"C:\Users\Administrator\Downloads\geckodriver-v0.30.0-win64\geckodriver.exe")
#driver.get("https://openqube.io/company/everis/")

books = driver.find_elements_by_class_name("booklink")
print(len(books))

count = 0
while True:
    if count==5:
        break
    count +=1
    print('page ',count)
    books = driver.find_elements_by_class_name('booklink')
    
    
    for book in books:
        try:
            name = book.find_elements_by_class_name('title')[0].text
            try:
                author = book.find_elements_by_class_name('subtitle')[0].text
            except:
                author = 'Not availbale'
            try:
                date = book.find_elements_by_class_name('extra')[0].text
            except:
                date = 'Not availbale'
            print('name:', name)
            print('author :', author)
            print('date :', date)
            print('_'*100)
        except:
            pass
        
    driver.find_elements_by_class_name('statusline')[0].find_elements_by_tag_name('a')[-1].click()
    print('|'*100)
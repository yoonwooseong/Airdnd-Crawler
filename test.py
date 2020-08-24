import requests
import time
from selenium import webdriver
from bs4 import BeautifulSoup
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'}

URL_BASE = "https://www.airbnb.co.kr/rooms/39804170?adults=1&location=%EA%B4%8C&check_in=2020-10-01&check_out=2020-10-03&source_impression_id=p3_1598247923_ydg6avDRJAlC0ViV"

driver = webdriver.Chrome('C:/Wooseong/web scraper/chromedriver')
driver.implicitly_wait(3)
driver.get(URL_BASE)
#driver.find_element_by_name('_mbmcsn') . click
html = driver.page_source
#result = requests.get(URL_BASE, headers = headers)
#soup = BeautifulSoup(result.text, "html.parser")
soup = BeautifulSoup(html, "html.parser")
notices = soup.select_one('.with-new-header')
abc = notices.select_one('._1cnse2m')
bc = abc.select_one('._14i3z6h')
print(bc)
#result = requests.get(URL_BASE, headers = headers)
#time.sleep(3)
#soup = BeautifulSoup(result.text, "html.parser")
##results = soup.select('._14i3z6h')
#print(soup)
#print(results)

from bs4 import BeautifulSoup
from urllib.parse import quote_plus
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_driver_path = "C:/Wooseong/web scraper/chromedriver.exe"

URL_BASE = "https://www.airbnb.co.kr/rooms/"
URL_PARAM = "?check_in=2020-10-01&check_out=2020-10-03"

driver = webdriver.Chrome()

def extract_detail2(accommodation_idxs):
    for room_idx in accommodation_idxs:
        room = room_idx
        URL = URL_BASE+room+URL_PARAM
        driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=chrome_driver_path)
        while True:
            driver.implicitly_wait(10)
            driver.get(URL)
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')

            results = soup.find("div", {"class","_1h6n1zu"})
            

            if results is not None:
                
                room_pictures = soup.find("div", {"class","_1h6n1zu"})
                room_price = soup.select_one('._ymq6as > _pgfqnw').string

                room_picture = room_pictures.find("picture")

                # print부분은 나중에 함수로 따로 빼기 !!
                print()
                print(URL)
                print(room_price)
                print(room_picture)
                print()
                break;
                
            else:
                print("try again")
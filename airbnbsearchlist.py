import requests
from bs4 import BeautifulSoup

URL = "https://www.airbnb.co.kr/s/%EA%B4%8C/homes?checkin=2020-10-01&checkout=2020-10-03&adults=1&children=0&infants=0"
#adults=1&children=0&infants=0

def get_last_page():
    set_last_page = 4
    return int(set_last_page)

def extract_room_idx(last_page):
    room_infos = []
    for page in range(last_page):
        print("Scraping the titles of page", page+1,"...")
        result = requests.get(f"{URL}&items_offset={page*20}")
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("div", {"class":"_3gn0lkf"})
        
        for result in results:
            result_url = result.find("a")["href"]
            room_price = result.find("span", {"class":"_1p7iugi"}).get_text()
            room_idx = result_url[result_url.index('s/')+2:result_url.index('?')]
            room_info = {"room_idx":room_idx, "room_price":room_price}
            room_infos.append(room_info)
    
    return room_infos

def get_accommodation_infos():
    last_page = get_last_page()
    room_infos = extract_room_idx(last_page)
    return room_infos


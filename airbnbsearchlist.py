import requests
from bs4 import BeautifulSoup

URL = "https://www.airbnb.co.kr/s/%EA%B4%8C/homes?checkin=2020-10-01&checkout=2020-10-03&adults=1&children=0&infants=0"

def get_last_page():
    set_last_page = 1
    return int(set_last_page)

def extract_room_idx(last_page):
    room_idxs = []
    for page in range(last_page):
        result = requests.get(f"{URL}&items_offset={page*20}")
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("div", {"class":"_3gn0lkf"})
        for result in results:
            result_url = result.find("a")["href"]
            room_idx = result_url[result_url.index('s/')+2:result_url.index('?')]
            print(room_idx)
            room_idxs.append(room_idx)
    
    return room_idxs

def get_accommodation_idxs():
    last_page = get_last_page()
    room_idxs = extract_room_idx(last_page)
    return room_idxs


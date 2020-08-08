import requests
from bs4 import BeautifulSoup

URL = "https://www.airbnb.co.kr/rooms/"

def extract_detail(accommodation_idxs):
    for room_idx in accommodation_idxs:
        room = room_idx

        while True:
            result = requests.get(f"{URL}"+room)
            soup = BeautifulSoup(result.text, "html.parser")
            results = soup.find("div",{"class","_tqmy57"})
            if results is not None:
                roominfo1, roominfo2 = results.find_all("div", recursive=False)
                print(roominfo1.string , roominfo2.string)
                break;
            else:
                print("try again")

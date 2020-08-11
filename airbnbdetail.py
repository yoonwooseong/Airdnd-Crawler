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
                room_name = soup.find("div", {"class","_mbmcsn"}).find("h1").get_text(strip=True)
                room_scores = soup.find("span", {"class","_1jpdmc0"})

                if room_scores is not None:
                    room_score = room_scores.get_text(strip=True)
                else:
                    room_score = 0.00

                room_review_nums = soup.find("span", {"class","_1sqnphj"})
                if room_review_nums is not None:
                    room_review_num = room_review_nums.get_text(strip=True)
                else:
                    room_review_num = "(0)"

                room_types , room_options = results.find_all("div", recursive=False)
                room_type = room_types.get_text(strip=True)
                room_option = room_options.get_text(strip=True)
                print()
                print(room_name)
                print(room_score, room_review_num)
                print(room_type)
                print(room_option)
                print()
                break;
            else:
                print("try again")

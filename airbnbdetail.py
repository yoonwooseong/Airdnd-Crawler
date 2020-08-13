import requests
from bs4 import BeautifulSoup

URL_BASE = "https://www.airbnb.co.kr/rooms/"
URL_PARAM = "?check_in=2020-08-01&check_out=2020-08-03"

def extract_detail(accommodation_idxs):
    for room_idx in accommodation_idxs:
        room = room_idx
        URL = URL_BASE+room+URL_PARAM

        while True:
            result = requests.get(f"{URL}")
            soup = BeautifulSoup(result.text, "html.parser")
            results = soup.find("div",{"class","_tqmy57"})
            # room_pictures = soup.find("div", {"class","_1h6n1zu"})

            if results is not None:

                room_name = soup.find("div", {"class","_mbmcsn"}).find("h1").get_text(strip=True)
                room_scores = soup.find("span", {"class","_1jpdmc0"})

                # None일때 오류 방지
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
                room_rules_sort = soup.find_all("div", {"class","_1qsawv5"})
                room_rules_content = soup.find_all("div", {"class","_1jlr81g"})
                room_price = soup.find("div", {"class","_ymq6as"})
                
                # room_picture = room_pictures.find("picture")

                # print부분은 나중에 함수로 따로 빼기 !!
                print()
                print(URL)
                print(room_name)
                print(room_score, room_review_num)
                print(room_type)
                print(room_option)
                print(room_rules_sort)
                print(room_rules_content)
                print(room_price)
                # print(room_picture)
                print()
                break;
            else:
                print("try again")

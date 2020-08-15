import cx_Oracle
import os
from urllib.parse import quote_plus

import requests
from bs4 import BeautifulSoup

#####한글깨짐 방지###### 
os.environ["NLS_LANG"] = ".AL32UTF8"
# DB와 연결된 코드
conn = cx_Oracle.connect('test/1111@localhost:1521/xe')
print(conn.version)

URL_BASE = "https://www.airbnb.co.kr/rooms/"
URL_PARAM = "?check_in=2020-10-01&check_out=2020-10-03"

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
                    room_score = "0.00"

                room_review_nums = soup.find("span", {"class","_1sqnphj"})
                if room_review_nums is not None:
                    room_review_num = room_review_nums.get_text(strip=True)
                else:
                    room_review_num = "(0)"

                room_types , room_options = results.find_all("div", recursive=False)
                room_type = room_types.get_text(strip=True)
                room_option = room_options.get_text(strip=True)
                #room_rules_sort = soup.find_all("div", {"class","_1044tk8"})
                room_rules_sort = soup.select('._1044tk8 > ._1mqc21n > ._1qsawv5')
                room_rules_sort_cont = soup.select('._1044tk8 > ._1mqc21n > ._1jlr81g')
                #room_rules_content = soup.find_all("div", {"class","_1jlr81g"})
                #room_price = soup.select_one('._pgfqnw')
                # room_price = soup.find("div", {"class","_ymq6as"})
                
                # room_picture = room_pictures.find("picture")

                # print부분은 나중에 함수로 따로 빼기 !!
                print()
                print(URL)
                print(room_name)
                print(room_score, room_review_num)
                print(room_type)
                print(room_option)
                j = 0
                for i in room_rules_sort:               
                    print(room_rules_sort[j].string)
                    print(room_rules_sort_cont[j].string)
                    j += 1
                
                
                
                #print(room_rules_content[0])
                #print(room_price)
                # print(room_picture)
                print()

                #요기 sql_insert = 'insert into airdnd_acom VALUES(seq_airdnd_acom_idx.nextVal, :ROOM_NAME, :ROOM_SCORE, :ROOM_REVIEW_NUM, :ROOM_TYPE)'
                #요기 db = conn.cursor()

                # encode 디비에 들어가기는 하나... 이상한 값이 출력됨
                # encode()로 변환한다음 decode()로 한글 변환한다.

                # 여기에 DB에 값이 있으면 건너뛰는 코드를 넣어줘야함
                
                #요기 db.execute(sql_insert, ROOM_NAME=room_name.encode('utf8').decode('utf8'), ROOM_SCORE=room_score.encode('utf8').decode('utf8'), 
                #                        ROOM_REVIEW_NUM=room_review_num.encode('utf8').decode('utf8'), ROOM_TYPE=room_type.encode('utf8').decode('utf8'))
                #요기 conn.commit()
                break;
                
            else:
                print("try again")


    db.close()
    conn.close()

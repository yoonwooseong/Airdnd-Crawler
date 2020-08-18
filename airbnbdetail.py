import cx_Oracle
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus

#####한글깨짐 방지###### 
os.environ["NLS_LANG"] = ".AL32UTF8"
# DB와 연결된 코드
conn = cx_Oracle.connect('test/1111@localhost:1521/xe')
print(conn.version)

URL_BASE = "https://www.airbnb.co.kr/rooms/"
URL_PARAM = "?check_in=2020-10-01&check_out=2020-10-03"
take_out_start_index = 0

def take_out_list(extracted_list):
    for e_list in extracted_list:               
        print(e_list.string)

def take_out_list_get_text(extracted_list):
    for e_list in extracted_list:               
        print(e_list.find("div").get_text())
        

def take_out_list_two(first_extracted_list, second_extracted_list):
    take_out_start_index = 0
    for f_list in first_extracted_list:               
        print(f_list.string, " : ", second_extracted_list[take_out_start_index].string)
    take_out_start_index = 0

def check_room_idx_in_DB():
    sql_select = 'select room_idx from airdnd_acom'
    db = conn.cursor()
    db.execute(sql_select)
    room_nums_in_DB = db.fetchall()
    return room_nums_in_DB
    
def extract_detail(accommodation_infos):
    room_nums_in_DB = check_room_idx_in_DB()
    
    for room_info in accommodation_infos:
        room_idx = room_info["room_idx"]

        if tuple([int(room_idx)]) not in room_nums_in_DB:
            room_price = room_info["room_price"]
            URL = URL_BASE+room_idx+URL_PARAM
            
            while True:
                result = requests.get(f"{URL}")
                soup = BeautifulSoup(result.text, "html.parser")
                results = soup.find("div",{"class","_tqmy57"})
                # room_pictures = soup.find("div", {"class","_1h6n1zu"})

                if results is not None:
                    room_name = soup.find("div", {"class","_mbmcsn"}).find("h1").get_text(strip=True)
                    room_location = soup.find("a", {"class","_5twioja"}).get_text()
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
                    room_rules_sort = soup.select('._1044tk8 > ._1mqc21n > ._1qsawv5')
                    room_rules_sort_cont = soup.select('._1044tk8 > ._1mqc21n > ._1jlr81g')

                    #room_rules_refund = soup.select('._8alet26')
                    #room_rules_refund_cont = soup.select('._8alet26 > ._1mqc21n > ._1jlr81g')
                    #room_host_talk = soup.find("div",{"class", "_1y6fhhr"})
                    room_bed_sort = soup.select('._9342og > ._1auxwog')
                    room_bed_sort_cont = soup.select('._9342og > ._1a5glfg')
                    
                    room_convenient_facilities = soup.select('._19xnuo97 > ._1nlbjeu')

                    room_scores_sort = soup.select('._a3qxec > ._y1ba89')
                    room_scores_sort_num = soup.select('._a3qxec > ._bgq2leu > ._4oybiu')

                    room_reviews = soup.select('._50mnu4')
                    # room_picture = room_pictures.find("picture")

                    # print부분은 나중에 함수로 따로 빼기 !!
                    print()
                    print(URL)
                    print(room_name, room_idx)
                    print(room_location)
                    print(room_price)
                    print(room_score, room_review_num)
                    print(room_type)
                    print(room_option)
                    take_out_list_two(room_rules_sort, room_rules_sort_cont)
                    take_out_list_two(room_bed_sort, room_bed_sort_cont)
                    take_out_list_get_text(room_convenient_facilities)
                    take_out_list_two(room_scores_sort, room_scores_sort_num)
                    take_out_list(room_reviews)
                    print()
                    # print(room_picture)
                    #print(room_rules_refund)
                    #print(room_rules_refund_cont)

                    #DB에 접근하기 위한 쿼리문
                    sql_insert = 'insert into airdnd_acom VALUES(seq_airdnd_acom_idx.nextVal, :ROOM_NAME, :ROOM_SCORE, :ROOM_REVIEW_NUM, :ROOM_TYPE ,:ROOM_IDX)'
                    db = conn.cursor()

                    #DB에 값이 없으면 저장
                    db.execute(sql_insert, ROOM_NAME=room_name.encode('utf8').decode('utf8'), ROOM_SCORE=room_score.encode('utf8').decode('utf8'), 
                                    ROOM_REVIEW_NUM=room_review_num.encode('utf8').decode('utf8'), ROOM_TYPE=room_type.encode('utf8').decode('utf8'), ROOM_IDX=room_idx)
                    conn.commit()
                    
                    break;
                else:
                    print("try again..")
        else:
            print("방번호 ", room_idx, "는 이미 저장되어 있습니다.")

    db.close()
    conn.close()

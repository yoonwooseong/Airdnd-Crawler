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
db = conn.cursor()

def extract_pictures(room_pictures):
    i = 0
    for picture in room_pictures:
        room_picture = picture.find("img").attrs['src']
        print(room_picture)
        i += 1
        if i == 5:
            break; 

def take_out_list(extracted_list):
    for e_list in extracted_list:               
        print(e_list.string)

def take_out_list_get_text_pre(extracted_list):
    for e_list in extracted_list:               
        print(e_list.find_all("div"))

def take_out_list_get_text(extracted_list):
    for e_list in extracted_list:               
        print(e_list.find("div").get_text())

def take_out_list_get_text_span(extracted_list):
    for e_list in extracted_list:               
        print(e_list.find("span", recursive=False).get_text())   

def take_out_list_two(first_extracted_list, second_extracted_list):
    take_out_start_index = 0
    for f_list in first_extracted_list:               
        print(f_list.string, " : ", second_extracted_list[take_out_start_index].string)
    take_out_start_index = 0

def check_room_idx_in_DB():
    sql_select = 'select room_idx from airdnd_acom'
    db.execute(sql_select)
    room_nums_in_DB = db.fetchall()
    return room_nums_in_DB
    
def extract_detail(accommodation_infos):
    room_nums_in_DB = check_room_idx_in_DB()
    
    for room_info in accommodation_infos:
        room_idx = room_info["room_idx"]

        if tuple([int(room_idx)]) not in room_nums_in_DB:
            price = room_info["room_price"]
            URL = URL_BASE+room_idx+URL_PARAM
            
            while True:
                result = requests.get(f"{URL}")
                soup = BeautifulSoup(result.text, "html.parser")
                results = soup.find("div",{"class","_tqmy57"})
                # room_pictures = soup.find("div", {"class","_1h6n1zu"})

                if results is not None:
                    main_title = soup.find("div", {"class","_mbmcsn"}).find("h1").get_text(strip=True)
                    addr = soup.find("a", {"class","_5twioja"}).get_text()
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

                    sub_titles , room_options = results.find_all("div", recursive=False)
                    sub_title = sub_titles.get_text(strip=True)
                    room_option = room_options.get_text(strip=True)
                    room_rules_sort = soup.select('._1044tk8 > ._1mqc21n > ._1qsawv5')
                    room_rules_sort_cont = soup.select('._1044tk8 > ._1mqc21n > ._1jlr81g')

                    room_host = soup.select_one('._1y6fhhr').find("span").get_text()
                    room_loc_info = soup.select('._1cvivhm > ._1byskwn > ._vd6w38n')
                    room_loc_info2 = soup.select('._1cvivhm > ._1byskwn')[0].find_all("div",{"class","_162hp8xh"})
                    
                    #만약 지역 설명이 없으면
                    if len(room_loc_info) == 1:
                        print("거리")
                        room_loc_info_cont = ""
                        room_loc_info_dist = room_loc_info[0].select('._175nxr3')
                    else:
                        print("둘다")
                        room_loc_info_cont = room_loc_info2[0].select('._1y6fhhr')#.find("span").get_text() #얘는 context 한개
                        room_loc_info_dist = soup.select_one('._17k42na').select('._175nxr3') #얘는 결과값 여러개 = 리스트

                    room_rules_prev = soup.select('._m9x7bnz')
                    room_use_rules = room_rules_prev[0].select('._ud8a1c > ._u827kd')
                    room_safety = room_rules_prev[1].select('._ud8a1c > ._u827kd')
                    
                    room_pictures = soup.find_all("div", {"class","_1h6n1zu"})
                    #room_picture1 = room_pictures[0].find("img").attrs['src']
                    #room_picture2 = room_pictures[1].find("img").attrs['src']
                    #room_picture3 = room_pictures[2].find("img").attrs['src']
                    #room_picture4 = room_pictures[3].find("img").attrs['src']
                    #room_picture5 = room_pictures[4].find("img").attrs['src']

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
                    print(main_title, room_idx)
                    print(addr)
                    print(price)
                    print(room_score, room_review_num)
                    print(sub_title)
                    print(room_option)
                    take_out_list_two(room_rules_sort, room_rules_sort_cont)
                    print("room_host : ", room_host)
                    print()
                    print("room_loc_info_cont : ", room_loc_info_cont)
                    take_out_list_get_text_pre(room_loc_info_dist)
                    take_out_list_two(room_bed_sort, room_bed_sort_cont)
                    take_out_list_get_text(room_convenient_facilities)
                    take_out_list_two(room_scores_sort, room_scores_sort_num)
                    take_out_list(room_reviews)
                    take_out_list_get_text_span(room_use_rules)
                    print()
                    take_out_list_get_text_span(room_safety)
                    print()
                    extract_pictures(room_pictures)
                    #print(room_picture1)
                    #print(room_picture2)
                    #print(room_picture3)
                    #print(room_picture4)
                    #print(room_picture5)
                    print()
                    #print(room_rules_refund)
                    #print(room_rules_refund_cont)

                    #DB에 접근하기 위한 쿼리문
                    sql_insert = 'insert into airdnd_acom VALUES(seq_airdnd_acom_idx.nextVal, :ROOM_NAME, :ROOM_SCORE, :ROOM_REVIEW_NUM, :ROOM_TYPE ,:ROOM_IDX)'

                    #DB에 값이 없으면 저장
                    db.execute(sql_insert, ROOM_NAME=main_title.encode('utf8').decode('utf8'), ROOM_SCORE=room_score.encode('utf8').decode('utf8'), 
                                    ROOM_REVIEW_NUM=room_review_num.encode('utf8').decode('utf8'), ROOM_TYPE=sub_title.encode('utf8').decode('utf8'), ROOM_IDX=room_idx)
                    conn.commit()
                    
                    break;
                else:
                    print("try again..")
        else:
            print("방번호 ", room_idx, "는 이미 저장되어 있습니다.")

    db.close()
    conn.close()

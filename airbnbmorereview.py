import pymysql
import os
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from urllib.parse import quote_plus

#####한글깨짐 방지###### 
os.environ["NLS_LANG"] = ".AL32UTF8"

# DB와 연결된 코드
conn = pymysql.connect(host = '52.78.111.36', user = 'root', password = '1111', db = 'AirdndDB', charset = 'utf8mb4', use_unicode=True)

URL_BASE = "https://www.airbnb.co.kr/rooms/"
db = conn.cursor()
def insert_room_data_in_airdnd_home_review(room_idx, review_dic):
    
    sql_insert =  'insert into airdnd_home_review (idx, home_idx, user_name, review_date, review_content, room_cleanliness, room_accuracy, room_communication, room_position, room_checkin, room_cost_effectiveness) VALUES (0, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
    val = (room_idx, review_dic['room_reviews_name'], review_dic['room_reviews_date'], review_dic['room_reviews_cont'], review_dic['room_cleanliness'], 
                review_dic['room_communication'], review_dic['room_position'], review_dic['room_accuracy'], review_dic['room_checkin'],
                review_dic['room_cost_effectiveness'])
    db.execute(sql_insert, val)
    conn.commit()
    print("DB저장 성공 - airdnd_review")

def extract_review(room_idx, extracted_list, room_rating):
    data_list = []
    for e_list in extracted_list:               
        room_reviews_name_date = e_list.select_one('div._1oy2hpi').find("div",{"class", "_1lc9bb6"}, recursive=False).get_text()
        room_reviews_name = room_reviews_name_date[:room_reviews_name_date.find("년 ")-4]
        room_reviews_date = e_list.select_one('div._1oy2hpi > div._1lc9bb6 > div').string
        room_reviews_cont = e_list.select_one('div._1y6fhhr > span').get_text()
        room_cleanliness = room_rating[0]
        room_accuracy = room_rating[1]
        room_communication = room_rating[2]
        room_position = room_rating[3]
        room_checkin = room_rating[4]
        room_cost_effectiveness = room_rating[5]

        review_dic = {'room_reviews_name':room_reviews_name, 'room_reviews_date':room_reviews_date ,'room_reviews_cont':room_reviews_cont, 
                    'room_cleanliness':room_cleanliness, 'room_accuracy':room_accuracy, 'room_communication':room_communication, 'room_position':room_position,
                    'room_checkin':room_checkin, 'room_cost_effectiveness':room_cost_effectiveness}

        insert_room_data_in_airdnd_home_review(room_idx, review_dic)
        data_list.append(review_dic)
    print("reviews : ", data_list)  
    return data_list

def extract_reviews_rating(room_idx, room_rating_num):
    data_list = []
    for e_list in room_rating_num:
        rating = float(e_list.string)
        data_list.append(rating)
    if len(data_list) == 0:
        data_list = [0, 0, 0, 0, 0, 0]
    print("data_list : ", data_list)
    return data_list

def scrape_reviews(URL, room_idx, place):
    while True:
        driver = webdriver.Chrome('C:/Wooseong/web scraper/chromedriver')
        driver.implicitly_wait(3)
        driver.get(URL)
        time.sleep(5)
        driver.implicitly_wait(15)
        scr1 = driver.find_element_by_xpath('/html/body/div[11]/section/div/div/div[3]/div/div/section/div/div[2]')
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scr1)

        time.sleep(3)
        html = driver.page_source
        time.sleep(3)
        soup = BeautifulSoup(html, "html.parser")
        results = soup.select_one('body.with-new-header')
        main_container = results.select_one('div._yzu7qn')
        load_test = main_container.select_one('div._m5uolq')
        
        #크롤링 소스 가져오기
        if load_test is not None:
            
            room_reviews = main_container.select('div._1gjypya')
            # 세부 별점
            room_rating_num = main_container.select('div._a3qxec > div._tk5b0r > span._4oybiu')
            
            print()
            room_rating = extract_reviews_rating(room_idx, room_rating_num)
            room_review = extract_review(room_idx, room_reviews, room_rating)
            print()

            data = {'room_idx':room_idx, 'room_reviews':room_review }
            driver.quit()
            return data
            
        else:
            print("try again..")
            driver.quit()


def extract_more_review(accommodation_infos):
    Query = accommodation_infos['Query']
    place = Query['place']
    checkin = Query['checkin']
    checkout = Query['checkout']
    adults = Query['adults']

    for room_info in accommodation_infos['room_infos']:
        room_idx = room_info["room_idx"]

        URL = URL_BASE+room_idx+"/reviews"+"?adults="+adults+"&location="+place+"&check_in="+checkin+"&check_out="+checkout+"&source_impression_id=p3_1598247923_ydg6avDRJAlC0ViV"
        scrape_reviews(URL, room_idx, place)

    db.close()
    conn.close()

# Airdnd Crawler 
##### 에어비엔비 크롤러

<br>

> **[Airdnd](https://github.com/DEVengersAssemble/airdnd-backend)** DEVengersAssemble/Airbnb clone cording 프로젝트에 필요한 데이터들을 추출하기 위한 웹 크롤러 개발

 해당 웹 크롤러(Web scraper)는 airbnb의 숙소 정보를 스크래핑하여 데이터베이스에 저장한다. 동적 크롤링을 위해 Selenium과 BeautifulSoup4 라이브러리를 사용하고 단순 웹 애플리케이션을 구현하기 위해 Flask framework를 사용하였다. 스크랩후에 pymysql로 MySQL에 저장한다.

<br>

## 🛢 Stack 
**Python**, **Flask**, **MySQL**, **Selenium**, **Beautifulsoup4b**  

<br>

## 📽 사용 예제

**1)** **app.py에서 디버깅(F5)를 실행 후 http://localhost:5000/ 접속**   
<img src="https://user-images.githubusercontent.com/57824259/131431490-3d491793-fddc-43af-99d8-e2e956aa151a.PNG" alt="home" width="500"/>   

**2)** **해당 검색창에 각 조건을 입력해 Search 버튼을 클릭**  

**3)** **크롤링 후 DB에 저장**  
<img src="https://user-images.githubusercontent.com/57824259/93201112-b2c52200-f78b-11ea-9cbf-f5a5a1d4ff7e.PNG" alt="DB tables" width="200"/>
<img src="https://user-images.githubusercontent.com/57824259/91679946-a2eef080-eb84-11ea-9d07-95da581a785c.PNG" alt="home DB" width="500"/>
   
**4)** **스크래핑 완료 후 해당 화면(scrapepage.html)으로 이동**  
<img src="https://user-images.githubusercontent.com/57824259/131431496-4b949500-a0f0-4fad-941d-71fb7e844072.PNG" alt="scrapepage" width="500"/>
  
**5)** **해당 숙소의 리뷰도 스크래핑을 원하면 more review 버튼을 클릭**  
<img src="https://user-images.githubusercontent.com/57824259/131431494-98507078-6322-4d77-89f3-4ab50e6c62c3.PNG" alt="end" width="500"/>  

<br>

## 📌 동작 알고리즘

> 아래의 동작을 통해 얻은 데이터들을 가지고 Airbnb Clone Coding 프로젝트에 사용 [프로젝트 바로가기](https://github.com/DEVengersAssemble)  
<img src="https://user-images.githubusercontent.com/57824259/94338748-a1073880-002f-11eb-9576-0cf608661849.png" alt="scrape" width="400"/>  

<br>

## ⚙ 개발 환경 설정

```sh
pip install pymysql --DB
pip install selenium
pip install flask --framework
pip install bs4
pip install requests
```
<br>

## ❗ 제한 사항

해당 사이트의 html 즉, class name이나 구조가 변경되면 코드 수정이 필요  

<br>

## ✏ 코드 리뷰  

코드리뷰(Code Review)는 언제나 환영입니다. 😊

<br>

## 🧾 업데이트 내역  

* 1.0.0
    * UI 변경 및 config.py 작성
* 0.1.1
    * more review 추가
    * issue 해결 (이모트 가능)
* 0.1.0
    * 완료
    * issue : host 당부의 말에 이모트를 넣을 시 오류. ( -utf8mb4-로 전환 필요 )
* 0.0.1
    * 작업 진행 중

<br>

## 📃 정보

윤우성 –  dntjd851@naver.com

해당 레퍼지토리는 오직 공부목적이며 공부 목적 이외의 용도로 사용불가  
MIT 라이센스를 준수하며 ``LICENSE``에서 자세한 정보를 확인할 수 있습니다.

[https://github.com/yoonwooseong/github-link](https://github.com/yoonwooseong/)

<br>

## 👌 기여 방법

1. (<https://github.com/yourname/yourproject/fork>)을 포크합니다.
2. (`git checkout -b feature`) 명령어로 새 브랜치를 만드세요.
3. (`git commit -am 'Add some'`) 명령어로 커밋하세요.
4. (`git push origin feature`) 명령어로 브랜치에 푸시하세요. 
5. 풀리퀘스트를 보내주세요.


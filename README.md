# web-scraper (only study)
> -Airdnd-(DEVengersAssemble Airbnb clone cording)에 필요한 데이터들을 가져오기 위해 web-scraper개발

해당 web-scraper는 airbnb 숙소정보를 스크래핑하여 데이터베이스에 저장한다. 동적 크롤링을 위한 Selenium과 BeautifulSoup4를 사용해 스크래핑을 하였고 프레임워크는 Flask framework를 사용하였다. 스크랩후에 pymysql로 MySQL에 저장한다.

### Use
<img src="https://user-images.githubusercontent.com/57824259/91246509-f4fdd380-e78a-11ea-86f6-1f2ed5aa9e74.png" alt="Flask" width="100" height="100"/> <img src="https://user-images.githubusercontent.com/57824259/91246511-f6c79700-e78a-11ea-8c45-d9561831cf8c.png" alt="Python" width="100" height="100"/>



## 사용 예제

airdndscraper.py에서 디버깅(F5)를 실행 후 http://localhost:5000/으로 접속한다. 실행시 첫 화면(home.html)이다.
<img src="https://user-images.githubusercontent.com/57824259/91246721-92f19e00-e78b-11ea-8444-e29a5b89c477.png" alt="home" width="600"/>  
해당 검색창에 각 조건을 입력해 Search 버튼을 클릭한다.  
<img src="https://user-images.githubusercontent.com/57824259/91246723-9422cb00-e78b-11ea-950f-b9b96a4afdf9.png" alt="home search" width="600"/>

아래와 같이 스크래핑을 print하고 DB에 저장한다.  
<img src="https://user-images.githubusercontent.com/57824259/91679946-a2eef080-eb84-11ea-9d07-95da581a785c.PNG" alt="home DB" width="600"/>
  
스크래핑이 완료되면 해당 화면(scrapepage.html)으로 이동한다.  
<img src="https://user-images.githubusercontent.com/57824259/91679942-a1252d00-eb84-11ea-8ad9-227d5ee55cd6.PNG" alt="scrapepage" width="600"/>
  
해당 숙소의 리뷰도 스크래핑을 원하면 more review 버튼을 클릭한다.  
<img src="https://user-images.githubusercontent.com/57824259/91680172-6079e380-eb85-11ea-81d8-71c8434016d5.PNG" alt="end" width="600"/>  
  
## 개발 환경 설정

```sh
pip install pymysql --DB
pip install selenium
pip install flask --framework
pip install bs4
```

## 업데이트 내역
* 0.1.1
    * more review 추가
    * issue 해결 (이모트 가능)
* 0.1.0
    * 완료
    * issue : host 당부의 말에 이모트를 넣을 시 오류. ( -utf8mb4-로 전환 필요 )
* 0.0.1
    * 작업 진행 중

## 정보

윤우성 –  dntjd851@naver.com

해당 레퍼지토리는 오직 공부목적이며 공부 목적 이외의 용도로 사용불가
MIT 라이센스를 준수하며 ``LICENSE``에서 자세한 정보를 확인할 수 있습니다.

[https://github.com/yoonwooseong/github-link](https://github.com/yoonwooseong/)

## 기여 방법

1. (<https://github.com/yourname/yourproject/fork>)을 포크합니다.
2. (`git checkout -b feature`) 명령어로 새 브랜치를 만드세요.
3. (`git commit -am 'Add some'`) 명령어로 커밋하세요.
4. (`git push origin feature`) 명령어로 브랜치에 푸시하세요. 
5. 풀리퀘스트를 보내주세요.

<!-- Markdown link & img dfn's -->
[npm-image]: https://img.shields.io/npm/v/datadog-metrics.svg?style=flat-square
[npm-url]: https://npmjs.org/package/datadog-metrics
[npm-downloads]: https://img.shields.io/npm/dm/datadog-metrics.svg?style=flat-square
[travis-image]: https://img.shields.io/travis/dbader/node-datadog-metrics/master.svg?style=flat-square
[travis-url]: https://travis-ci.org/dbader/node-datadog-metrics
[wiki]: https://github.com/yourname/yourproject/wiki

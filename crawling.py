from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.dbtest

chromedriver = '/Users/lia/Downloads/chromedriver'
driver = webdriver.Chrome(chromedriver)
# selenium 라이브러리 기본 작업

driver.get('https://everytime.kr/login')
# 크롤링 할 홈페이지 가져오기
driver.find_element_by_name("userid").send_keys("lhr519")
# 태그의 네임이 userid 인 element 가져오고 "내 아이디" 입력
driver.find_element_by_name("password").send_keys("gofls0519")
# 태그의 네임이 password 인 element 가져오고 "비밀번호" 입력
driver.find_element_by_tag_name("input").send_keys(Keys.RETURN)
# 로그인 버튼 찾고 클릭

time.sleep(2)
driver.find_element_by_xpath('//*[@id="submenu"]/div/div[10]/ul/li[4]/a').click()
time.sleep(2)
driver.find_element_by_css_selector('#container > div.wrap.articles > div.pagination > a').click()
time.sleep(1)
# 맛집게시판 가능 경로로 이동하기

def next_page():
    driver.find_element_by_css_selector('#container > div.wrap.articles > div.pagination > a.next').click()
    time.sleep(0.5)

    res = driver.page_source
    soup = BeautifulSoup(res, "html.parser")
    article = soup.select('#container > div.wrap.articles > article > a > p')
    # 함수 next_page 생성, 게시판에서 내용 저장할 준비

    for mtjp_data in article:
        mtjp_text = mtjp_data.text
        mtjp = mtjp_text.split('/')
        if len(mtjp[0])<20:
            doc = {
                'name': mtjp[0]
            }
            db.everytime.insert_one(doc)

driver.find_element_by_xpath('//*[@id="sheet"]/ul/li[3]/a').click()
# 2페이지에 뜨는 광고창 1번 끄기

time.sleep(0.5)
for page_roof in range(100):
    next_page()
# next_page를 page_roof라는 폴더에 넣고 반복

driver.quit()
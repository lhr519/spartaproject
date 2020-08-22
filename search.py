import requests
import time
from pymongo import MongoClient

# 맛집 데이터는 seoul_matjip 이라는 데이터베이스에 저장하겠습니다.
client = MongoClient('localhost', 27017)
db = client.dbtest

# 데이터베이스의 맛집을 리스트로 가져오기
names = list(db.everytime.find({}, {'_id': False}))

# 네이버 검색 API 신청을 통해 발급받은 아이디와 시크릿 키를 입력합니다.
client_id = "HlpUUsPVK3nDzKI3TdSZ"
client_secret = "XlucMij7bd"


# 검색어를 전달하면 결과를 반환하는 함수
def get_naver_result(keyword):
    time.sleep(0.1)
    # url에 전달받은 검색어를 삽입합니다.
    api_url = f"https://openapi.naver.com/v1/search/local.json?query={keyword}&display=10&start=1&sort=random"
    # 아이디와 시크릿 키를 부가 정보로 같이 보냅니다.
    headers = {'X-Naver-Client-Id': client_id, 'X-Naver-Client-Secret': client_secret}
    # 검색 결과를 data에 저장합니다.
    data = requests.get(api_url, headers=headers)
    # 받아온 JSON 결과를 딕셔너리로 변환합니다.
    data = data.json()

    if (data['total'] == 0):
        return 0
    else:
        min = ((int(data['items'][0]['mapx'])-307190)**2+(int(data['items'][0]['mapy'])-551581)**2)
        index = 0

        for i in range(data['total']):
            difx = int(data['items'][i]['mapx']) - 307190
            dify = int(data['items'][i]['mapy']) - 551581
            dif = difx**2 + dify**2

            if (dif<min):
                min = dif
                index = i

        temp = {
            'title': data['items'][index]['title'].replace('<b>','').replace('</b>',''),
            'category': data['items'][index]['category'],
            'mapx': data['items'][index]['mapx'],
            'mapy': data['items'][index]['mapy'],
        }
        return temp


# 저장할 전체 맛집 목록입니다.
docs = []
# 구별로 검색을 실행합니다.
for name in names:
    mtjp = name['name']
    keyword = f'{mtjp}'
    # 맛집 리스트를 받아옵니다.
    search = get_naver_result(keyword)
    if (search != 0): #검색 결과가 있으면
        if (len(docs)==0): #검색 결과가 딱 하나 있으면
            docs.append(search)
        else: #검색 결과가 여러가지 있으면
            boo = 0
            for i in range(len(docs)):
                if (docs[i]['mapx']==search['mapx']): #중복 거르기
                    boo = 1
                    break

            if (boo==0): #처음 나오는 맛집 이름이면
                if '음식점' in search['category']:
                    docs.append(search)
                elif '양식' in search['category']:
                    docs.append(search)
                elif '일식' in search['category']:
                    docs.append(search)
                elif '이탈리아음식' in search['category']:
                    docs.append(search)
                elif '카페,디저트' in search['category']:
                    docs.append(search)
                elif '한식' in search['category']:
                    docs.append(search)
                elif '도시락,컵밥' in search['category']:
                    docs.append(search)
                elif '분식' in search['category']:
                    docs.append(search)
                elif '중식' in search['category']:
                    docs.append(search)
                elif '육류,고기요리' in search['category']:
                    docs.append(search)
                elif '술집' in search['category']:
                    docs.append(search)

# 맛집 정보를 저장합니다.
db.matjip.insert_many(docs)

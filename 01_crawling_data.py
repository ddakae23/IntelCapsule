from selenium import webdriver              # 웹사이트(및 웹 애플리케이션)의 유효성 검사에 사용되는 자동화 테스트 프레임워크
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import pandas as pd
import re
import time
import datetime

url = 'https://kr.iherb.com/'
options = ChromeOptions()
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
options.add_argument('user-agent=' + user_agent)
options.add_argument('lang=ko_KR')

# 크롬 드라이버 최신 버전 설정
service = ChromeService(executble_path=ChromeDriverManager().install())
# 크롬 드라이버
driver = webdriver.Chrome(service=service, options=options)

category = ['seasonal-allergies', 'sleep', 'weight-loss', 'childrens-health', 'mens-health', 'womens-health']
# pages = [14, 13, 14, 16, 8, 16]  # 각 카테고리 별 총 페이지 수
pages = [13, 13, 13, 13, 8, 13]    # 학습을 위해 최대 페이지를 중간 지점인 13 페이지로 제한함
df_titles = pd.DataFrame()

for i in range(6):
    # 카테고리 변경
    section_url = 'https://kr.iherb.com/c/{}'.format(category[i])
    df_titles = pd.DataFrame()
    titles = []                 # titles 초기화
    for j in range(1, pages[i]+1):       # pages[i]+1 (시간 문제 상 3으로 축소)
        if j == 1:
            url = section_url
        else:
            url = section_url + '?p={}'.format(j)        # 페이지 변경
        driver.get(url)
        time.sleep(2)
        for k in range(1, 10):
            try:
                print('%d'%k)
                xpath_temp = '/html/body/div[7]/div/div[3]/div/div/div[1]/div[1]/div[2]/div[2]/div[{}]/div/div[2]/div[1]/a'.format(k)
                driver.find_element('xpath', xpath_temp).click()
                time.sleep(2)
                print('debug01')

                # title = re.compile('[^가-힣|a-z|A-Z|0-9]').sub(' ', title)
                # titles.append(title)
                driver.back()
                time.sleep(5)

            except:
                # 오류가 발생할 경우 error + 카테고리, 페이지, 제품 번호 출력
                print('error {} {} {}'.format(i, j, k))

    df_section_title = pd.DataFrame(titles, columns=['titles'])
    df_section_title['category'] = category[i]
    df_titles = pd.concat([df_titles, df_section_title], ignore_index=True)

    # crawling 폴더에 Nutrients_(카테고리)_(년월일).cvs 파일로 저장
    df_titles.to_csv(
        './crawling_data/Nutrients_{}_{}.csv'.format(category[i], datetime.datetime.now().strftime('%Y%m%d')),
        index=False)

print(df_titles.head(20))  # 상위 제목 20개 출력
df_titles.info()
print(df_titles['category'].value_counts())


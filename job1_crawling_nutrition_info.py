import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import pandas as pd
import re
import time
import os

options = ChromeOptions()
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'
options.add_argument('user-agent='+user_agent)
options.add_argument('lang=ko_KR')

service = ChromeService(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
driver.maximize_window()

# 카테고리, 카테고리별 페이지 수
category = ['eye-vision', 'hair-skin-nails','heart','immune-support','pain-relief','respiratory-support']
category_ko = ['눈-시력','모발-피부-손톱','심혈관계','면역계','통증 완화','호흡기계']
pages = [9, 17, 17, 17, 9, 3]

for c in range(len(category)-1):
    descriptions = []
    df_descriptions = pd.DataFrame()
    category_url = 'https://kr.iherb.com/c/{}'.format(category[c])

    for page in range(1,pages[c]+1):
        page_url = category_url + '?p={}'.format(page)
        driver.get(page_url)
        time.sleep(3)

        # 한 페이지 내에 있는 영양제 개수
        products = driver.find_elements(By.CLASS_NAME,'product-cell-container')
        products = len(products)

        for idx in range(1,products+1):
            try:
                product_url = driver.find_element(By.XPATH,'/html/body/div[7]/div/div[3]/div/div/div[1]/div[1]/div[2]/div[2]/div[{}]/div/div[2]/div[1]/a'.format(idx)).click()
                time.sleep(5)
                description_text = ''
                # description_list = driver.find_elements(By.XPATH,'/html/body/div[8]/article/div[2]/div/section/div[2]/div/div/div[1]/div[1]/div/div/ul/li')
                description_p = driver.find_elements(By.XPATH,'/html/body/div[8]/article/div[2]/div/section/div[2]/div/div/div[1]/div[1]/div/div/p')
                # if description_list is not None:
                #     for description in description_list:
                #         description = re.compile('[^가-힣|a-z|A-Z|0-9]').sub(' ',description.text)
                #         description_text += description+' '
                if len(description_p) > 1:
                    description_p = description_p[:-1]
                for description in description_p:
                    if description.text is None:
                        continue
                    description = re.compile('[^가-힣|a-z|A-Z|0-9]').sub(' ',description.text)
                    description_text += description+' '
                print(description_text)
                descriptions.append(description_text)

                driver.back()
                time.sleep(3)
            except:
                print('Error {} {} page {}'.format(category[c], page, idx))

        if page % 2 == 0:
            df_description = pd.DataFrame(descriptions, columns=['description'])
            df_description['category'] = category_ko[c]
            df_descriptions = pd.concat([df_descriptions, df_description],ignore_index=True)
            if not os.path.isdir('./crawling_data'):
                os.mkdir('crawling_data')
            df_descriptions.to_csv('./crawling_data/nutrition_info_{}_{}.csv'.format(category_ko[c], page), index=False)
            descriptions = []

    df_description = pd.DataFrame(descriptions, columns=['description'])
    df_description['category'] = category_ko[c]
    df_descriptions = pd.concat([df_descriptions, df_description], ignore_index=True)
    df_descriptions.to_csv('./crawling_data/nutrition_info_{}_last.csv'.format(category_ko[c]), index=False)







import pandas as pd
import glob                 # 특정 파일 패턴이나 이름과 일치하는 파일을 검색
import datetime

# for 문 반복을 위해 카테고리 리스트 생성
category = ['seasonal-allergies', 'sleep', 'weight-loss', 'childrens-health', 'mens-health', 'womens-health']

for i in range(6):
    df = pd.read_csv('./crawling_data/nutrients_{}_20231018.csv'.format(category[i]))
    X = df['effect']
    Y = df['category']
    df = df.dropna()            # null 값 제거
    df.info()                   # null 값 제거 확인을 위해 정보 출력
    # null 값이 제거된 dataframe 을 cvs 형태로 저장
    df.to_csv('../crawling_data/remove_null/nutrients_{}_{}.csv'.format(category[i], datetime.datetime.now().strftime('%Y%m%d')),
        index=False)

# 반복문에서 저장한 cvs 파일을 불러옴
data_path = glob.glob('./crawling_data/remove_null/*')
print(data_path)

df = pd.DataFrame()
for path in data_path:
    df_temp = pd.read_csv(path)
    df = pd.concat([df, df_temp])
print(df.head())
print(df['category'].value_counts())
df.info()
df.to_csv('./crawling_data/nutrients_effects_{}.csv'.format(
    datetime.datetime.now().strftime('%Y%m%d')), index=False)
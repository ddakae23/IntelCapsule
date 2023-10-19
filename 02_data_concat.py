import pandas as pd
import glob                 # 특정 파일 패턴이나 이름과 일치하는 파일을 검색
import datetime

category = ['seasonal-allergies', 'sleep', 'weight-loss', 'childrens-health', 'mens-health', 'womens-health']

for i in range(6):
    df = pd.read_csv('./crawling_data/nutrients_{}_20231018.csv'.format(category[i]))
    X = df['effect']
    Y = df['category']
    df = df.dropna()
    df.info()
    df.to_csv('../crawling_data/remove_null/nutrients_{}_{}.csv'.format(category[i], datetime.datetime.now().strftime('%Y%m%d')),
        index=False)

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
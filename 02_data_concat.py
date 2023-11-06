import pandas as pd
import glob                 # 특정 파일 패턴이나 이름과 일치하는 파일을 검색
import datetime

# 반복문에서 저장한 cvs 파일을 불러옴
data_path = glob.glob('./crawling_data/*')
print(data_path)

df = pd.DataFrame()
for path in data_path:
    df_temp = pd.read_csv(path)
    df = pd.concat([df, df_temp])

X = df['effect']
Y = df['category']
Z = df['name']
df = df.dropna()

print(df.head())
print(df['category'].value_counts())

df.info()
df.to_csv('./crawling_data/nutrients_effects_{}.csv'.format(
    datetime.datetime.now().strftime('%Y%m%d')), index=False)


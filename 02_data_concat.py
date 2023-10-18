import pandas as pd
import glob                 # 특정 파일 패턴이나 이름과 일치하는 파일을 검색
import datetime

# 지정 폴더 속 data path 전체 출력
data_path = glob.glob('./crawling_data/*')
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
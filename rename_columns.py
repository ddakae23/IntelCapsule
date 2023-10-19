import pandas as pd
import datetime

# category = ['눈-시력', '면역계', '모발-피부-손톱', '심혈관계', '통증 완화', '호흡기계']
category = ['anti-aging-longevity', 'ayurveda', 'bladder', 'bone-joint-cartilage', 'brain-cognitive', 'circulatory-support']
category_kr = ['노화 장수','아유르베다','방광', '뼈 관절 연골', '두뇌 인지', '순환기계']
# for i in range(6):
#     df = pd.read_csv('./crawling_data/crawling_data_{}_20231019.csv'.format(category[i]))
#     df = df.rename(columns={'comments': 'effect'})
#     # df = df.rename(columns={'description': 'effect'})
#     df.to_csv(
#         './crawling_data/nutrients_{}_{}.csv'.format(category[i], datetime.datetime.now().strftime('%Y%m%d')),
#         index=False)
df = pd.read_csv('./crawling_data/nutrients_effects_20231019.csv')
for i in range(len(category)):
    df['category'] = df['category'].replace({category[i]:category_kr[i]})
df['category'] = df['category'].replace({'눈-시력':'눈 시력'})
df['category'] = df['category'].replace({'모발-피부-손톱':'모발 피부 손톱'})
df.to_csv('./crawling_data/nutrients_effects_{}.csv'.format(datetime.datetime.now().strftime('%Y%m%d')))
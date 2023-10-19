import pandas as pd
import datetime

# category = ['눈-시력', '면역계', '모발-피부-손톱', '심혈관계', '통증 완화', '호흡기계']
category = ['anti-aging-longevity', 'ayurveda', 'bladder', 'bone-joint-cartilage', 'brain-cognitive', 'circulatory-support']
for i in range(6):
    df = pd.read_csv('./crawling_data/crawling_data_{}_20231019.csv'.format(category[i]))
    df = df.rename(columns={'comments': 'effect'})
    # df = df.rename(columns={'description': 'effect'})
    df.to_csv(
        './crawling_data/nutrients_{}_{}.csv'.format(category[i], datetime.datetime.now().strftime('%Y%m%d')),
        index=False)

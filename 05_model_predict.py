import pandas as pd
import numpy as np
import pickle           # 파이썬에서 사용하는 dic, list, class과 같은 자료형을 변환 없이 그대로 파일로 저장하고 이를 불러올 때 사용
from sklearn.model_selection import train_test_split        # pip install scikit-learn
from sklearn.preprocessing import LabelEncoder              # 범주형 변수를 숫자 형식으로 변환
from konlpy.tag import Okt                                  # 한국어 형태소 분석
# tensorflow ver 2.7.0 downgrade
from tensorflow.keras.utils import to_categorical           # 정수형(integer) 레이블을 원-핫 인코딩(one-hot encoding) 벡터로 변환
from tensorflow.keras.preprocessing.text import Tokenizer   # 자연어 처리에서 입력 문장을 일정한 단위로 분할
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import load_model

df = pd.read_csv('./crawling_data/predict.csv')
print(df.head())
df.info()

X = df['effect']
Y = df['category']

with open('./models/encoder.pickle', 'rb') as f:        # rb : read binary
    encoder = pickle.load(f)
labeled_y = encoder.transform(Y)                        # 주의 : fit을 할 경우 정보를 새로 받게됨
label = encoder.classes_

onehot_y = to_categorical(labeled_y)
# print(onehot_y)

okt = Okt()

for i in range(len(X)):
    X[i] = okt.morphs(X[i], stem=True)
stopwords = pd.read_csv('./stopwords.csv', index_col=0)

for j in range(len(X)):                                         # title 수 만큼 반복
    words = []
    for i in range(len(X[j])):                                  # 형태소? 수 만큼 반복
        if len(X[j][i]) > 1:                                    # 한글자 제거
            if X[j][i] not in list(stopwords['stopword']):      # 불용어 확인
                words.append(X[j][i])
    X[j] = ' '.join(words)

with open('./models/nutrients_token.pickle', 'rb') as f:
    token = pickle.load(f)

tokened_x = token.texts_to_sequences(X)

# 최대 길이 제한
for i in range(len(tokened_x)):
    if len(tokened_x[i]) > 170:
        tokened_x[i] = tokened_x[i][:171]
x_pad = pad_sequences(tokened_x, 170)
model = load_model('./models/nutrients_category_classification_model_0.7203791737556458.h5')

preds = model.predict(x_pad)
predicts = []
for pred in preds:
    most = label[np.argmax(pred)]
    pred[np.argmax(pred)] = 0
    second = label[np.argmax(pred)]
    predicts.append([most, second])
df['predict'] = predicts    # list 로 두 개의 값을 제출 (가장 높은 확률, 두번째로 높은 확률의 답)
print(df.head(30))

df['OX'] = 0                # 두 개의 답 중 하나라도 맞췄을 확률
for i in range(len(df)):
    if df.loc[i, 'category'] in df.loc[i, 'predict']:
        df.loc[i, 'OX'] = 'O'
    else :
        df.loc[i, 'OX'] = 'X'
print(df['OX'].value_counts())
print(df['OX'].value_counts()/len(df))

for i in range(len(df)):    # 오답 확인
    if df['category'][i] not in df['predict'][i]:
        print(df.iloc[i])

# for i in range(len(df)):    # 정답 확인
#     if df['category'][i] in df['predict'][i]:
#         print(df.iloc[i])
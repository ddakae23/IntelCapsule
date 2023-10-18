import pandas as pd
import numpy as np
import pickle           # 파이썬에서 사용하는 dic, list, class과 같은 자료형을 변환 없이 그대로 파일로 저장하고 이를 불러올 때 사용
from sklearn.model_selection import train_test_split        # pip install scikit-learn
from sklearn.preprocessing import LabelEncoder              # 범주형 변수를 숫자 형식으로 변환
from konlpy.tag import Okt                                  # 한국어 형태소 분석
# tensorflow ver 2.7.0 downgrade!
from tensorflow.keras.utils import to_categorical           # 정수형(integer) 레이블을 원-핫 인코딩(one-hot encoding) 벡터로 변환
from tensorflow.keras.preprocessing.text import Tokenizer   # 자연어 처리에서 입력 문장을 일정한 단위로 분할
from tensorflow.keras.preprocessing.sequence import pad_sequences

df = pd.read_csv('./crawling_data/nutrients_effects_{}.csv')

X = df['effect']
Y = df['category']

encoder = LabelEncoder()
labeled_y = encoder.fit_transform(Y)
label = encoder.classes_
print(labeled_y[:3])

with open('./models/encoder.pickle', 'wb') as f:
    pickle.dump(encoder, f)

    okt = Okt()

for i in range(len(X)):
    X[i] = okt.morphs(X[i], stem=True)
# print(X)

# 불용어 리스트 불러옴 (인덱스 제거)
stopwords = pd.read_csv('./stopwords.csv', index_col=0)
for j in range(len(X)):                                         # title 수 만큼 반복
    words = []
    for i in range(len(X[j])):                                  # 형태소? 수 만큼 반복
        if len(X[j][i]) > 1:                                    # 한글자 제거
            if X[j][i] not in list(stopwords['stopword']):      # 불용어 확인
                words.append(X[j][i])
    X[j] = ' '.join(words)
# print(X)

token = Tokenizer()
token.fit_on_texts(X)                               # 각 형태소에 라벨 부여
tokened_x = token.texts_to_sequences(X)             # 라벨에 리스트 부여
wordsize = len(token.word_index) + 1
print("Tokened_X :", tokened_x[0:3])
print("Wordsize :", wordsize)

with open('./models/nutrients_token.pickle', 'wb') as f:        # wb : write binary
    pickle.dump(token, f)

max = 0             # max 초기화
for i in range(len(tokened_x)):
    if max < len(tokened_x[i]):
        max = len(tokened_x[i])
print("가장 긴 문장의 길이 : ", max)

x_pad = pad_sequences(tokened_x, max)               # 모든 문장의 길이를 가장 긴 문장의 길이에 맞춤 (빈 공간의 값 = 0)
# print(x_pad[:3])

X_train, X_test, Y_train, Y_test = train_test_split(
    x_pad, onehot_y, test_size=0.2)
print(X_train.shape, Y_train.shape)
print(X_test.shape, Y_test.shape)

xy = X_train, X_test, Y_train, Y_test
np.save('./crawling_data/nutrients_data_max_{}_wordsize_{}'.format(max, wordsize), xy)
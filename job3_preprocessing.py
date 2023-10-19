import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from konlpy.tag import Okt
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.utils import to_categorical
import pickle
import os

pd.set_option('display.unicode.east_asian_width',True)
df_descriptions = pd.read_csv('./crawling_data/nutrients_effects_20231019.csv')
df_descriptions.dropna(inplace=True)

X = df_descriptions['effect']
Y = df_descriptions['category']

okt = Okt()
for i in range(len(X)):
    try:
        X[i] = okt.morphs(X[i],stem=True)
        if i % 100 == 0:
            print('Morphs: {} / {}'.format(i, len(X)))
    except:
        continue

stopwords = pd.read_csv('./stopwords.csv', index_col=0)
for i in range(len(X)):
    try:
        words = []
        for j in range(len(X[i])):
            if len(X[i][j]) > 1:
                if X[i][j] not in list(stopwords['stopword']):
                    words.append(X[i][j])
        if len(words) >=10:
            X[i] = ' '.join(words)
        else:
            X[i] = None
            Y[i] = None
        if i % 100 == 0:
            print('Stopwords remove: {} / {}'.format(i, len(X)))
    except:
        continue

# 유사한 문장 제거
X = np.array(X)

import difflib
for i in range(len(X)-1):
    if X[i] is not None and X[i+1] is not None:
        X_bytes = bytes(X[i],'utf-8')
        Y_bytes = bytes(X[i+1], 'utf-8')
        X_bytes_list = list(X_bytes)
        Y_bytes_list = list(Y_bytes)
        sim = difflib.SequenceMatcher(None, X_bytes_list, Y_bytes_list)
        similar = sim.ratio()
        if similar >= 0.9:
            X[i+1] = None
            Y[i+1] = None
    if i % 100 == 0:
        print('remove similar sentence: {} / {}'.format(i, len(X)))

X = pd.Series(X)
X = X.dropna()
Y = Y.dropna()
X.to_csv('./crawling_data/preprocessing.csv',index=False)

encoder = LabelEncoder()
label_Y = encoder.fit_transform(Y)
label = encoder.classes_
print(label)
onehot_Y = to_categorical(label_Y)

if not os.path.isdir('./models'):
    os.mkdir('models')
with open('./models/encoder.pickle','wb') as f:
    pickle.dump(encoder, f)

token = Tokenizer()
token.fit_on_texts(X)
tokened_X = token.texts_to_sequences(X)
wordsize = len(token.word_index) + 1

with open('./models/news_token.pickle', 'wb') as f:
    pickle.dump(token, f)

# 제일 긴 문장의 길이에 맞게 다른 문장들을 패딩
max_length = len(max(tokened_X, key=len))
tokened_X_pad = pad_sequences(tokened_X, max_length)

# train, test 데이터 생성 및 저장
train_X, test_X, train_Y, test_Y = train_test_split(tokened_X_pad, onehot_Y, test_size=0.2)
print(train_X.shape, train_Y.shape)
print(test_X.shape, test_Y.shape)

xy = train_X, test_X, train_Y, test_Y
np.save('./models/nutrition_info_max_{}_wordsize_{}'.format(max_length, wordsize), xy)
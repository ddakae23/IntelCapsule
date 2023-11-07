import pandas as pd
import numpy as np
import pickle  # 파이썬에서 사용하는 dic, list, class과 같은 자료형을 변환 없이 그대로 파일로 저장하고 이를 불러올 때 사용
from sklearn.model_selection import train_test_split  # pip install scikit-learn
from sklearn.preprocessing import LabelEncoder  # 범주형 변수를 숫자 형식으로 변환
from konlpy.tag import Okt  # 한국어 형태소 분석
from tensorflow.keras.preprocessing.text import Tokenizer  # 자연어 처리에서 입력 문장을 일정한 단위로 분할
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.utils import to_categorical  # 정수형(integer) 레이블을 원-핫 인코딩(one-hot encoding) 벡터로 변환
from difflib import SequenceMatcher

# 크롤링 데이터 불러오기
df = pd.read_csv('./crawling_data/nutrients_effects_20231106.csv')
stopwords = pd.read_csv('./stopwords.csv', index_col=0)
stopwords = list(stopwords['stopword'])

# 변수 선언
cleaned_sentence = ''
cleaned_sentences = []
# 상품명 데이터를 배열로 변환
Z = np.array(df.name)
for i in range(len(Z) - 48):
    if Z[i] is not None:
        for j in range(i - 48, i + 48):
            if i != j and Z[j] is not None:
                ratio = SequenceMatcher(None, Z[i], Z[j]).ratio()  # 두 제품 명을 비교하여 유사성을 구함
                if ratio >= 0.9:                            # 유사성이 90% 이상일 경우 두번째 상품 제거
                    # print('similar data,{} :{}'.format(i, Z[i]))
                    # print('remove data,{} :{}'.format(j, Z[j]))
                    df.effect[j] = None
                    df.category[j] = None
                    df.name[j] = None
df.dropna(inplace=True)
df.reset_index(inplace=True)

okt = Okt()

for i in range(len(df.effect)):
    tk_x = okt.pos(df.effect[i], stem=True)
    df_token = pd.DataFrame(tk_x, columns=['word', 'class'])
    # df_token = df_token[
    #     ((df_token['class'] == 'Alpha') | (df_token['class'] == 'Noun') | (df_token['class'] == 'Verb') | (df_token['class'] == 'Adjective'))]
    df_token = df_token[
        ((df_token['class'] == 'Noun') | (df_token['class'] == 'Verb') | (df_token['class'] == 'Adjective'))]
    words = []
    for word in df_token.word:
        if 1 < len(word):
            if word not in stopwords:
                words.append(word)
                cleaned_sentence = ' '.join(words)
    if len(cleaned_sentence.split()) < 15:
        cleaned_sentence = None
    cleaned_sentences.append(cleaned_sentence)
df['cleaned_sentences'] = cleaned_sentences

df.drop(labels=['effect','index'], axis=1, inplace=True)
df.dropna(inplace=True)
df.to_csv('./crawling_data/preprocessing.csv', index=False)
# df.info()
print(df['category'].value_counts())
encoder = LabelEncoder()
labeled_y = encoder.fit_transform(df.category)
label = encoder.classes_
onehot_y = to_categorical(labeled_y)

with open('./models/encoder.pickle', 'wb') as f:
    pickle.dump(encoder, f)

token = Tokenizer()
token.fit_on_texts(df.cleaned_sentences)  # 각 형태소에 라벨 부여
tokened_x = token.texts_to_sequences(df.cleaned_sentences)  # 라벨에 리스트 부여
wordsize = len(token.word_index) + 1
print("Tokened_X :", tokened_x[0:3])
print("Wordsize :", wordsize)

len_max = 0  # max 초기화
for i in range(len(tokened_x)):
    if len_max < len(tokened_x[i]):
        len_max = len(tokened_x[i])
print("가장 긴 문장의 길이 : ", len_max)

x_pad = pad_sequences(tokened_x, len_max)  # 모든 문장의 길이를 가장 긴 문장의 길이에 맞춤 (빈 공간의 값 = 0)
print(x_pad[:20])

X_train, X_test, Y_train, Y_test = train_test_split(
    x_pad, onehot_y, test_size=0.2)
print(X_train.shape, Y_train.shape)
print(X_test.shape, Y_test.shape)

xy = X_train, X_test, Y_train, Y_test
np.save('./crawling_data/nutrients_data_max_{}_wordsize_{}'.format(len_max, wordsize), xy)
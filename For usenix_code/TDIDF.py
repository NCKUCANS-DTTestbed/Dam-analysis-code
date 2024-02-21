#!/usr/bin/python
# -*- coding: UTF-8 -*-

import jieba
import jieba.posseg as pseg
import os
import sys
import pandas as pd
from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer

if __name__ =="__main__":
    word_df = pd.read_csv('./Dataset_3.csv')
    temp = word_df['Functiongram'].tolist()
    temp = [str(x)[:-2] for x in temp]
    temp = [','.join(temp)]
    #corpus = temp.flatten()
    #temp = [y for x in temp for y in x]

    print(temp)
    corpus = temp

    vectorizer = CountVectorizer()
    transformer = TfidfTransformer()
    tfidf=transformer.fit_transform(vectorizer.fit_transform(corpus))

    word = vectorizer.get_feature_names()
    weight = tfidf.toarray()

    for i in range(len(weight)):
        print("--------------這裡輸出第"+str(i))

        for j in range(len(word)):
            print(word[j],weight[i][j])
            #word_df.TFfun[str(word_df.Functiongram) == word[j]] = weight[i][j]
            #word_df.ix[str(word_df['Functiongram']) == word[j], 'TFfun'] = weight[i][j]

            #word_df['Functiongram'] = word_df['Functiongram'].apply(str)
            #word_df[True, 'TFfun'] = "9999"
            word_df.ix[word_df.Functiongram == float(word[j]), 'TFfun'] = weight[i][j]
            # data.Function[(data.IP_src == '192.168.1.101') | (data.IP_dst == '192.168.1.105')] = 3.4

        word_df['Functiongram'] = word_df['Functiongram'].apply(str)
        word_df.to_csv('Dataset_3.csv')
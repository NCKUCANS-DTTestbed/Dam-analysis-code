#!/usr/bin/python
# -*- coding: UTF-8 -*-

import pandas as pd
import os
from sklearn import svm
import math
from sklearn import preprocessing
from keras.models import Model
from pandas.tseries.holiday import USFederalHolidayCalendar as calendar
from keras.layers import Dense, Input
import datetime as dt
import math


if __name__ =="__main__":
    packetDF = pd.read_csv('./Dataset_4.csv')
    packetDF = packetDF.sort_values('No')
    # one-hot-encoder
    ProtocolData = pd.get_dummies(packetDF['IP_src'])
    ProtocolData.index = range(len(ProtocolData))
    # auto-encoder
    input_1 = Input((4,))
    encoded = Dense(2, activation='relu')(input_1)
    encoder_output = Dense(2)(encoded)
    decoded = Dense(4, activation='relu')(encoder_output)
    autoencoder_week = Model(input=input_1, output=decoded)

    autoencoder_week.compile(optimizer='adam', loss='mse')
    autoencoder_week.fit(ProtocolData, ProtocolData,
                         nb_epoch=128,
                         batch_size=100,
                         shuffle=True)
    encoder_week = Model(input_1, encoded)
    weekdayDF = encoder_week.predict(ProtocolData)
    weekdayDF = pd.DataFrame(weekdayDF, columns=['IP_src1', 'IP_src2'])
    print("aaaa")

    packetDF['IP_src1'] = weekdayDF['IP_src1']
    packetDF['IP_src2'] = weekdayDF['IP_src2']
    print('aaaa')
    packetDF = packetDF.sort_values('No')
    packetDF = packetDF.fillna(0)
    packetDF.to_csv('Dataset_4.csv')
    #packetDF = pd.concat([packetDF, weekdayDF], axis=1)

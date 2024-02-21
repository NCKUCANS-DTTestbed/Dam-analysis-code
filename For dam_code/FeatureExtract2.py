#!/usr/bin/python
# -*- coding: UTF-8 -*-

import json
import csv
import pandas as pd
from pandas import Series,DataFrame

# abnormal dataset

data = pd.read_csv('Dataset_1.csv')    #abnormal
#data2 = pd.read_csv('Dataset_2.csv')   #normal
result_DF = pd.read_csv('Dataset_ok1.csv')   #result
print(result_DF.shape)
print("------------------------------------------------------------------------------------------------")
#thresh filter
#time_DF = DataFrame([])
# time elapsed

ip_list = list(set(data['IP_src']))
pro_list = list(set(data['Protocol']))
time_DF = DataFrame([])
for k in pro_list:
    if(k == 'modbus'):
        print(1111)
    for i in ip_list:
        for j in ip_list:

            test_DF = result_DF.loc[(((result_DF['IP_src'] == i) & (result_DF['IP_dst'] == j)) |
                                     ((result_DF['IP_src'] == j) & (result_DF['IP_dst'] == i)))
                                & (result_DF.Protocol == k)]
            test_DF['Trela1'] = test_DF['Trela'].shift(1)
            test_DF['Trela_fun'] = test_DF['Trela'] - test_DF['Trela1']
            time_DF = pd.concat([time_DF, test_DF ],axis=0, ignore_index=True)

time_DF = time_DF.drop_duplicates()
time_DF = time_DF.sort_values('Unnamed: 0')

print(time_DF.shape)
print("------------------------------------------------------------------------------------------------")

time_DF2 = DataFrame([])
for j in pro_list:
    #test_DF = result_DF.loc[(result_DF.Protocol == j)]
    test_DF = time_DF.loc[(time_DF.Protocol == j)]
    test_DF['Trela1'] = test_DF['Trela'].shift(1)
    test_DF['Trela_pro'] = test_DF['Trela'] - test_DF['Trela1']
    time_DF2 = pd.concat([time_DF2, test_DF ],axis=0, ignore_index=True)

time_DF2 = time_DF2.drop_duplicates()
print(time_DF.shape)
time_DF2.to_csv('Dataset_3.csv')


print('Over')

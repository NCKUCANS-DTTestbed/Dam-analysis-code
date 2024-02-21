#!/usr/bin/python
# -*- coding: UTF-8 -*-

import json
import csv
import pandas as pd
from pandas import Series,DataFrame

#AnswerDF =  pd.read_csv('Answer.csv')

#AnswerDF['Answer'] = AnswerDF['Answer'].apply(lambda x:x[-1:])

# abnormal dataset
with open('Dataset_1.csv', 'w',) as csvfile:

    writer = csv.writer(csvfile)
    writer.writerow(['No', 'Trela','Protocol','IP_src','IP_dst','Tdelta','Function1','Function2','Function3',
                     'Function4','Function5','Function6','Trela1','Trela_fun','Function-gram','TFfun','Answer'])
    with open('shigangdam_attack.json', 'r',encoding="utf-8") as f:
        Json_data = json.load(f)

    for item in Json_data:

        packetnum = item['_source']['layers']['frame']['frame.number']
        Tdelta = item['_source']['layers']['frame']['frame.time_delta']
        Trela = item['_source']['layers']['frame']['frame.time_relative']
        protocol = item['_source']['layers']['frame']['frame.protocols'].split(":")
        protocol = protocol[-1]

        if("ip" in item['_source']['layers'].keys()):
            dst_ip = item['_source']['layers']['ip']['ip.src']
            src_ip = item['_source']['layers']['ip']['ip.dst']
        else:
            dst_ip = 0
            src_ip = 0

        if ("modbus" in item['_source']['layers'].keys()):
            function = item['_source']['layers']['modbus']['modbus.func_code']
            writer.writerow([packetnum, Trela, protocol, dst_ip, src_ip, Tdelta, function ])
        elif("tcp" in item['_source']['layers'].keys()):
            function = item['_source']['layers']['tcp']['tcp.flags']
            function = function[-2:]
            writer.writerow([packetnum, Trela, protocol, dst_ip, src_ip, Tdelta, function])
        else:
            writer.writerow([packetnum, Trela, protocol, dst_ip, src_ip, Tdelta, 0])




print('----------------------')

data = pd.read_csv('Dataset_1.csv')    #abnormal
#data['Answer'] = AnswerDF
#data2 = pd.read_csv('Dataset_2.csv')   #normal


#thresh1 = data.ix[data['IP_src'] == 0]
print(data.shape)
#thresh2 = \
#data[data['IP_src'] == '192.168.1.101', 'Function'] = "9999"

ip_list = list(set(data['IP_src']))
pro_list = list(set(data['Protocol']))


result_DF = DataFrame([])

for k in pro_list:
    for i in ip_list:
        for j in ip_list:

            test_DF = data.loc[(((data['IP_src'] == i) & (data['IP_dst'] == j)) | ((data['IP_src'] == j) & (data['IP_dst'] == i)))
                                & (data.Protocol == k)]
            test_DF['Function2'] = test_DF['Function1'].shift(1)
            test_DF['Function3'] = test_DF['Function1'].shift(2)
            test_DF['Function4'] = test_DF['Function1'].shift(3)
            test_DF['Function5'] = test_DF['Function1'].shift(4)
            test_DF['Function6'] = test_DF['Function1'].shift(5)
            result_DF = pd.concat([result_DF, test_DF ],axis=0, ignore_index=True)

            #data.Function1[(data.IP_src == i) | (data.IP_dst == j) & (data.Protocol == k)] = data['Function'].shift(1)
            #data.Function2[(data.IP_src == i) | (data.IP_dst == j) & (data.Protocol == k)] = data['Function'].shift(2)

result_DF = result_DF.drop_duplicates()
result_DF = result_DF.sort_values('No')
result_DF['Function-gram'] = result_DF['Function1']*10000000000\
                             +result_DF['Function2']*100000000\
                             +result_DF['Function3']*1000000\
                             +result_DF['Function4']*10000\
                             +result_DF['Function5']*100\
                             +result_DF['Function6']


print(result_DF.shape)
print("------------------------------------------------------------------------------------------------")
#thresh filter

result_DF = result_DF.fillna(0)
result_DF.to_csv('Dataset_ok1.csv')
print("------------------------------------------------------------------------------------------------")
#thresh filter
#time_DF = DataFrame([])
# time elapsed
for k in pro_list:
    for i in ip_list:
        for j in ip_list:

            test_DF = result_DF.loc[(((result_DF['IP_src'] == i) & (result_DF['IP_dst'] == j)) | ((result_DF['IP_src'] == j)
                                                                                         & (result_DF['IP_dst'] == i)))
                                                                                            & (result_DF.Protocol == k)]

            test_DF['Trela1'] = test_DF['Trela'].shift(1)
            result_DF['Trela_fun'] = test_DF['Trela'] - test_DF['Trela1']
            #time_DF = pd.concat([time_DF, test_DF ],axis=0, ignore_index=True)
            print("ok")

result_DF = result_DF.fillna(0)
result_DF.to_csv('Dataset_ok1.csv')

print(result_DF.shape)
print("------------------------------------------------------------------------------------------------")
print('Over')

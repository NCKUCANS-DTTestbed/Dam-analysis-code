from scipy.cluster.hierarchy import dendrogram, linkage
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np


data = pd.read_csv('Dataset_4.csv')
data = data[['Protocol','IP_src','Protocol1','Protocol2','Protocol3','IP_src1','IP_src2','TFfun','Trela_fun','Trela_pro','Answer']]
data = data.head(30000)
#data['Trela_pro'] = (data['Trela_pro'].apply(np.log))*10
data['Trela_pro'] = data['Trela_pro']
data['TFfun'] = data['TFfun']
data = data.fillna(0)

data.ix[(data.Trela_pro <= 0), 'Trela_pro'] = 0
data.ix[(data.Trela_fun <= 0), 'Trela_fun'] = 0


from sklearn.cluster import AgglomerativeClustering
#Trela_pro','Trela_fun'
cluster = AgglomerativeClustering(n_clusters=25, affinity='euclidean', linkage='ward')
group = cluster.fit_predict(data[['Protocol1','Protocol2','Protocol3','IP_src1','IP_src2','Trela_fun','Trela_pro','TFfun']])
result = pd.value_counts(group)
#,'Trela_fun'
#,'Trela_pro'
print(result)
print(cluster.labels_)

data.ix[data.Protocol1 == 8, 'Group'] = '0'
data[['Group']] = cluster.labels_
data.ix[data.Group == 0, 'Result'] = 1#0000000000
data.ix[data.Group == 1, 'Result'] = 1
data.ix[data.Group == 2, 'Result'] = 1
data.ix[data.Group == 3, 'Result'] = 1#xxxxxxxxxx
data.ix[data.Group == 4, 'Result'] = 1
data.ix[data.Group == 5, 'Result'] = 1
data.ix[data.Group == 6, 'Result'] = 1
data.ix[data.Group == 7, 'Result'] = 0
data.ix[data.Group == 8, 'Result'] = 0
data.ix[data.Group == 9, 'Result'] = 1
data.ix[data.Group == 10, 'Result'] = 1
data.ix[data.Group == 11, 'Result'] = 1
data.ix[data.Group == 12, 'Result'] = 1
data.ix[data.Group == 13, 'Result'] = 0
data.ix[data.Group == 14, 'Result'] = 0
data.ix[data.Group == 15, 'Result'] = 1
data.ix[data.Group == 16, 'Result'] = 0
data.ix[data.Group == 17, 'Result'] = 1
data.ix[data.Group == 18, 'Result'] = 0
data.ix[data.Group == 19, 'Result'] = 0
data.ix[data.Group == 20, 'Result'] = 1
data.ix[data.Group == 21, 'Result'] = 0
data.ix[data.Group == 22, 'Result'] = 1
data.ix[data.Group == 23, 'Result'] = 0
data.ix[data.Group == 24, 'Result'] = 0


data.ix[((data.Answer == 1)  & (data.Result == 1)  ), 'accu'] = 1  #TP 976
data.ix[((data.Answer == 1)  & (data.Result == 0)  ), 'accu'] = 2  #FN 223
data.ix[((data.Answer == 0)  & (data.Result == 0)  ), 'accu'] = 3  #TN 38640
data.ix[((data.Answer == 0)  & (data.Result == 1)  ), 'accu'] = 4  #FP 161

accu = data['accu']
accu = pd.value_counts(list(accu))
print(accu)
print('11')

tn = list(accu)[0]
fp = list(accu)[2]
tp = list(accu)[1]
fn = 0#list(accu)[3]

ACCU = (tp+tn) / (tp + fn + fp + tn)
RECALL = tp / (tp + fn)    # 0.814
PRECISION = tp / (tp + fp)  # 0.858
data.to_csv('Dataset_dam.csv')

print(ACCU)
print(RECALL)
print(PRECISION)
#ansDF.to_csv(str(i) + 'cityfinal_3.csv')


#plt.scatter(X[:,0],X[:,1], c=cluster.labels_, cmap='rainbow')
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul  1 00:41:01 2018

@author: davitisoselia
"""
from . import merger
from . import selected_features

import matplotlib as mpl
mpl.use('Agg')
modeln='bdt/fall_detection_1.h5' # model name
merged_path = 'bdt/merged.csv'
import os.path
import pickle

if not os.path.isfile(merged_path):
    print("merging ...")
    merger.merge()

falls=[] #saves fall start-end moments

with open(merged_path) as csv:
    content = csv.readlines()
print("preprocessing ...")    
for i in range(int(len(content))):
    if('tart' in content[i]):
        falls.append([i])
    if('nd' in content[i]):
        falls[-1].append(i)
    content[i] = content[i].split(',')

print("done rpeprocessing ...")
#content = content[::10]

'''

    if (len(content[i][-1]) > 2):
        print(i)
   ''' 
import numpy as np
import sys





def row_to_numpy(point):
    segment = []
    fell = [0]
    if (int(content[point][-2])) > 0:
        fell = [1]
    segment = (content[point][:-2])
    for j in range(len(segment)):
        segment[j] = float(segment[j])
    segment = np.array(segment)
    return segment, fell

ml,mk = row_to_numpy(5)


sensorNum = ml.shape[0]


'''
print(len((content[35232])))
'''
print(len(content[0]))



test_percentage = 0.8




import numpy as np

import random

def get_fall(point = 0, test = False):
    fell = [0]
    while fell == [0]:
        point = falls[random.randint(0, len(falls))][0] + random.randint(10, 100)
        if (test):
            point = falls[int(random.randint(len(falls)*test_percentage), len(falls) )][0] + random.randint(10, 100)
        else:
            point = falls[random.randint(0, int(len(falls)*test_percentage))][0] + random.randint(10, 100)
        segment , fell = row_to_numpy(point)
    return segment , fell


j = 0
iter = 0
balance_needed = False
lastnp = np.array([])
temp_storage = '43.39	11.03	16.21	85.62	178.8	172.6	40.39	18.69	7.767	137.4	105.2	107.9	59.82	107.9	51.32	206.8	54.73	56.91	34.09	29	46.25	49.62	47.7	96.14	83.78	178.1	178.8	87.09	82.72	177.8	178.8	136.2	135.6	18.03	37.27	39.53	28.23	35.61	37.22	3.644	67.37	21.58	63.19	82.38	82.69	178.9	82.62	180	180	86.57	180	179.7	80.72	179.9	80.44	79.99	107.7	179.8	89.15	178.1	-14.97	66.98	180	50.26	71.05	109.1	179.9	84.46	179.8	180	86.76	180	179.8	89.57	179.8	180	86.59	179.4	179.8	86.43	179.9	179.8	87.1	179.8	179.7	88.29	179.7	1791	1377	2042	1881	1604	958.5	2965	3014	2036	2325	2396	2078	3940	3616	3647	4682	3080	1474	3861	6624	2780	4152	4875	5995	3818	2253	641.1	3324	4992	5953	2714	3502	1516	8552	2113	1574	4586	15890	14370	4300	2691	1406	14470	10660	2981	11250	16000	14240	0.9126	0.4787	0.7286	0.8671	0.01697	0.8622	0.7929	-0.03522	0.3384	0.7069	0.6081	0.8366	0.7314	0.6626	0.7502	0.6727	0.6694	0.9436	0.2001	0.8859	0.04322	0.5211	0.9018	0.9656	0.9665	0.2635	0.9052	0.9012	0.7843	0.7929	0.4846	0.8235	0.7375	0.7812	0.6371	0.7238	0.4928	0.4771	0.8543	0.7993	0.8932	0.6572	0.4866	0.01178	0.1309	0.718	0.7586	0.7251'.split('	')
normalizer = [] 
for value in temp_storage:
    normalizer.append(float(value))
temp_storage = np.array(normalizer)


from numpy import loadtxt
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
'''
np_arr, y = get_fall() if False else row_to_numpy(5)
np_arr = np_arr / temp_storage
y_train = np.array(y)
x_train = np.transpose(np_arr).reshape(1,sensorNum)

# fit model no training data
model = XGBClassifier()
model.fit(x_train, y_train)
y_pred = model.predict(x_train)
predictions = [round(value) for value in y_pred]
'''


confusion_matrix = [[0,0],[0,0]]
def checkresult_confusion(point = random.randint(1, len(content)-50), length = random.randint(300, 1500), check_fall = False, confusion_matrix = [[0,0],[0,0]]):
    np_arr, y = get_fall() if check_fall else row_to_numpy(point)
    np_arr = np_arr / temp_storage
    y_train = np.array(y)
    x_train = np.transpose(np_arr).reshape(1,sensorNum)
    prediction = model.predict(x_train)
    #print(y_train)
    #print(prediction)
    if (y_train[0]==round(prediction[0][0]) and y_train[0] == 1):
        confusion_matrix[0][0] += 1
    elif (y_train[0]==round(prediction[0][0]) and y_train[0] == 0):
        confusion_matrix[1][1] += 1
    elif (y_train[0]!=round(prediction[0][0]) and y_train[0] == 0):
        confusion_matrix[1][0] += 1
    elif (y_train[0]!=round(prediction[0][0]) and y_train[0] == 1):
        confusion_matrix[0][1] += 1
    return (y_train[0]==round(prediction[0][0])), confusion_matrix

modeln='a.h5'

def test():
    matrix = [[0,0],[0,0]]
    fall = True    
    correct = 0
    i = 0
    while i < 100:
        try:
            temp, matrix = checkresult_confusion(check_fall = fall, confusion_matrix =matrix )
            correct += (temp)            
            i+=1
            fall = not fall
        except:
            print(sys.exc_info()[0])
    
    print('accuracy: ')
    print(correct)
    print(matrix)
X = []
Y = []
iter = 0
# prep numpy for random forest
balance_needed = False
print("start training ...")
while(iter<2000):
    j=random.randint(1, int((len(content)-50)))
    #print(j)
    #avred = not avred
    try:
        #print(iter)
        #print('Balance 0 : ' + str(balance_needed))
        if balance_needed:
            np_arr, y = get_fall()
        else:
            np_arr, y = row_to_numpy(j)
        #print('Balance : ' + str(balance_needed))
        lastnp = np_arr
        np_arr = np_arr / temp_storage
        y_train = np.array(y)
        x_train = np.transpose(np_arr).reshape(sensorNum)
        X.append(x_train)
        Y.append(y_train)
        iter+=1;
        balance_needed = not balance_needed
    except (TypeError,IndexError):
        print('error raised at index ' +str(j))
        print(sys.exc_info()[0])
        pass
    except:
        print(sys.exc_info()[0])
        raise
print("finished training ...")


j = 0
iter = 0
balance_needed = False
lastnp = np.array([])

X_1 = []
Y_1 = []
iter = 0
# prep numpy for random forest
balance_needed = False
while(iter<400):
    j=random.randint(1, int((len(content)-50)))
    #print(j)
    #avred = not avred
    try:
        #print(iter)
        #print('Balance 0 : ' + str(balance_needed))
        if balance_needed:
            np_arr, y = get_fall()
        else:
            np_arr, y = row_to_numpy(j)
        #print('Balance : ' + str(balance_needed))
        lastnp = np_arr
        np_arr = np_arr / temp_storage
        y_train = np.array(y)
        x_train = np.transpose(np_arr).reshape(sensorNum)
        X_1.append(x_train)
        Y_1.append(y_train)
        iter+=1;
        balance_needed = not balance_needed
    except (TypeError,IndexError):
        print('error raised at index ' +str(j))
        print(sys.exc_info()[0])
        pass
    except:
        print(sys.exc_info()[0])
        raise

 
X_t = np.array(X)
Y_t = np.array(Y)
Y_t = Y_t.reshape(Y_t.shape[0])
X_test = np.array(X_1)
Y_test = np.array(Y_1)
Y_test = Y_test.reshape(Y_test.shape[0])

'''
model = XGBClassifier()
model.fit(X_t, Y_t, eval_metric='auc')
'''
model = XGBClassifier()
eval_set = [(X_t, Y_t), (X_test, Y_test)]

model.fit(X_t, Y_t, eval_metric=["error", "logloss"], eval_set=eval_set, verbose=True)

from matplotlib import pyplot

y_pred = model.predict(X_t)
predictions = [round(value) for value in y_pred]
# evaluate predictions
accuracy = accuracy_score(Y_t, predictions)
print("Training Accuracy: %.2f%%" % (accuracy * 100.0))
import sklearn
print(sklearn.metrics.precision_score(Y_t, predictions))
print(sklearn.metrics.recall_score(Y_t, predictions))

y_pred = model.predict(X_test)
predictions = [round(value) for value in y_pred]
# evaluate predictions
accuracy = accuracy_score(Y_test, predictions)
print("Accuracy: %.2f%%" % (accuracy * 100.0))
# retrieve performance metrics
results = model.evals_result()
with open('bdt_log.pkl', 'wb') as f:
    pickle.dump(results, f)
epochs = len(results['validation_0']['error'])
x_axis = range(0, epochs)
# plot log loss
fig, ax = pyplot.subplots()
ax.plot(x_axis, results['validation_0']['logloss'], label='Train')
ax.plot(x_axis, results['validation_1']['logloss'], label='Test')
ax.legend()
pyplot.ylabel('Log Loss')
pyplot.title('XGBoost Log Loss')
pyplot.savefig('f2.png')
# plot classification error
fig, ax = pyplot.subplots()
ax.plot(x_axis, results['validation_0']['error'], label='Train')
ax.plot(x_axis, results['validation_1']['error'], label='Test')
ax.legend()
pyplot.ylabel('Classification Error')
pyplot.title('XGBoost Classification Error')
pyplot.savefig('bdt_acc.png')





'''


























y_pred = model.predict(X_test)
predictions = [round(value) for value in y_pred]
# evaluate predictions
accuracy = accuracy_score(Y_test, predictions)
print("Testing Accuracy: %.2f%%" % (accuracy * 100.0))
import sklearn
print(sklearn.metrics.precision_score(Y_test, predictions))
print(sklearn.metrics.recall_score(Y_test, predictions))


from sklearn.metrics import roc_curve
from sklearn.metrics import auc
import matplotlib.pyplot as plt
import numpy as np

#log_y = bdt.Y_test
#log_predicted = bdt.y_pred

log_y = Y_test
log_predicted = y_pred

#log_y = np.array([1, 1, 0, 0])
#log_predicted =  np.array([0.1, 0.4, 0.35, 0.8])
fpr, tpr, thresholds = roc_curve(log_y, log_predicted, pos_label  = 1)
roc_auc = auc(log_y, log_predicted, reorder  = True)


# Plot ROC curve
#plt.plot(fpr, tpr, label='ROC curve (area = %0.3f)' % roc_auc)
plt.plot(fpr, tpr, label='ROC curve GBT')
plt.plot([0, 1], [0, 1], 'k--')  # random predictions curve
#plt.xlim([0.0, 1.0])
#plt.ylim([0.0, 1.0])
plt.xlabel('False Positive Rate or (1 - Specifity)')
plt.ylabel('True Positive Rate or (Sensitivity)')
plt.title('Receiver Operating Characteristic')
plt.legend(loc="lower right")
plt.savefig('ignore.png')
#finish

'''
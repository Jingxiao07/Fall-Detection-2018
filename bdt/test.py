# -*- coding: utf-8 -*-
"""
Created on Fri Jul  6 02:59:38 2018

@author: Dati
"""

import merger
from keras.models import load_model


temp_storage = '43.39	11.03	16.21	85.62	178.8	172.6	40.39	18.69	7.767	137.4	105.2	107.9	59.82	107.9	51.32	206.8	54.73	56.91	34.09	29	46.25	49.62	47.7	96.14	83.78	178.1	178.8	87.09	82.72	177.8	178.8	136.2	135.6	18.03	37.27	39.53	28.23	35.61	37.22	3.644	67.37	21.58	63.19	82.38	82.69	178.9	82.62	180	180	86.57	180	179.7	80.72	179.9	80.44	79.99	107.7	179.8	89.15	178.1	-14.97	66.98	180	50.26	71.05	109.1	179.9	84.46	179.8	180	86.76	180	179.8	89.57	179.8	180	86.59	179.4	179.8	86.43	179.9	179.8	87.1	179.8	179.7	88.29	179.7	1791	1377	2042	1881	1604	958.5	2965	3014	2036	2325	2396	2078	3940	3616	3647	4682	3080	1474	3861	6624	2780	4152	4875	5995	3818	2253	641.1	3324	4992	5953	2714	3502	1516	8552	2113	1574	4586	15890	14370	4300	2691	1406	14470	10660	2981	11250	16000	14240	0.9126	0.4787	0.7286	0.8671	0.01697	0.8622	0.7929	-0.03522	0.3384	0.7069	0.6081	0.8366	0.7314	0.6626	0.7502	0.6727	0.6694	0.9436	0.2001	0.8859	0.04322	0.5211	0.9018	0.9656	0.9665	0.2635	0.9052	0.9012	0.7843	0.7929	0.4846	0.8235	0.7375	0.7812	0.6371	0.7238	0.4928	0.4771	0.8543	0.7993	0.8932	0.6572	0.4866	0.01178	0.1309	0.718	0.7586	0.7251'.split('	')
normalizer = [] 
for value in temp_storage:
    normalizer.append(float(value))
temp_storage = np.array(normalizer)

modeln='fall_detection_1.h5' # model name
merged_path = 'merged.csv'
import os.path
model = load_model('a1.h5')

if not os.path.isfile(merged_path):
    merger.merge()
    
modeln='fall_detection_1.h5' # model name
merged_path = 'merged.csv'
import os.path

if not os.path.isfile(merged_path):
    merger.merge()

falls=[] #saves fall start-end moments

with open('merged.csv') as csv:
    content = csv.readlines()
for i in range(len(content)):
    if('tart' in content[i]):
        falls.append([i])
    if('nd' in content[i]):
        falls[-1].append(i)
    content[i] = content[i].split(',')



import numpy as np
import numpy as np
import sys



def generate_numpy(point, length = 500):
    segment = []
    falls = 0;
    fell = [[0,1]]
    for i in range(point, point + length):
        if ('all' in content[i][-1]):
            falls+=1
        if i%10==0:
            segment.append(content[i][:-2])
    if (falls == 1):
        return
    elif(falls>1):
        fell = [[1,0]]
    for i in range(len(segment)):
        for j in range(len(segment[i])):
            segment[i][j] = float(segment[i][j])
    segment = np.array(segment)
    return segment, fell

ml,mk = generate_numpy(5)







sensorNum = ml.shape[1]



print(len((content[35232])))
print(len(content[0]))




import random


def get_fall(point = 0, length = random.randint(300, 1500)):
    if point == 0:
        point = falls[random.randint(0, len(falls))][0] - random.randint(100, 500)
    segment , fell = generate_numpy(point, length)
    return segment , fell
'''
def checkresult(point = random.randint(1, len(content)-50), length = random.randint(300, 1500), check_fall = False):
    np_arr, y = get_fall() if check_fall else generate_numpy(point, length)
    np_arr = np_arr / temp_storage
    x_train = np.transpose(np_arr).reshape(1,np_arr.shape[0],np_arr.shape[1])
    #x_train = temp_storage / 50
    y_train = np.array(y)
    prediction = model.predict(x_train)
    #print(y_train)
    #print(prediction)
    return (np.argmax(y_train)==np.argmax(prediction))
'''
confusion_matrix = [[0,0],[0,0]]
def checkresult_confusion(point = random.randint(1, len(content)-50), length = random.randint(300, 1500), check_fall = False):
    np_arr, y = get_fall() if check_fall else generate_numpy(point, length)
    np_arr = np_arr / temp_storage
    x_train = np.transpose(np_arr).reshape(1,np_arr.shape[0],np_arr.shape[1])
    #x_train = temp_storage / 50
    y_train = np.array(y)
    prediction = model.predict(x_train)
    print(y_train)
    print(prediction)
    if (np.argmax(y_train)==np.argmax(prediction) and np.argmax(y_train) == 0):
        confusion_matrix[0][0] += 1
    elif (np.argmax(y_train)==np.argmax(prediction) and np.argmax(y_train) == 1):
        confusion_matrix[1][1] += 1
    elif (np.argmax(y_train)!=np.argmax(prediction) and np.argmax(y_train) == 1):
        confusion_matrix[1][0] += 1
    elif (np.argmax(y_train)!=np.argmax(prediction) and np.argmax(y_train) == 0):
        confusion_matrix[0][1] += 1
    return (np.argmax(y_train)==np.argmax(prediction))

'''
def checkresult(point = random.randint(1, len(content)-50), length = random.randint(300, 1500), check_fall = False):
    np_arr, y = get_fall() if check_fall else generate_numpy(point, length)
    x_train = np.transpose(np_arr).reshape(1,np_arr.shape[0],np_arr.shape[1])
    x_train = x_train / temp_storage
    y_train = np.array(y)
    print(y_train)
    return (np.argmax(y_train)==np.argmax(model.predict(x_train)))
'''
def test():
    fall = True    
    correct = 0
    i = 0
    while i < 1000:
        try:
            
            correct += (checkresult_confusion(check_fall = fall))
            i+=1
            fall = not fall
        except:
            print(sys.exc_info()[0])
    
    print(correct)


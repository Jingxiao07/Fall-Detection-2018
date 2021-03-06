import os
from glob import glob

#current directory
top = os.getcwd() + '/CSV_fall_data/**/*.csv'
directory = 'RNN/'

#takes path to csv, returns csv as string stripped of the metadata
def strip(path):
    end = False
    start= False
    with open(path) as csv:
        content = csv.readlines()
    stripped = ""
    i = 0
    last = ""
    for row in content:
        if (i==4):
            if ('Marker' not in row):
                end = True
            if ('Switch' in row):
                start = True
        if (i > 5):
            new_row = row
            if (end):
                new_row = new_row[:-1]+',0,\n'
            new_row = new_row.split(',')
            if(start):
                new_row = new_row[3:]
            else:
                 new_row = new_row[1:]
            new_row = ','.join(new_row)
            last = new_row
            stripped += new_row
        i+=1
        if (i%10000 == 0):
            print('progress ' + str(i) + '/' + str(len(content)))
            pass
    print(path + str(len(last.split(','))))
    return stripped



#takes path with CSV files parent folder, merges into single CSV file. As default searches in current directory and outputs to merged.csv
def merge(path = os.getcwd() + '/CSV_fall_data/**/*.csv', mergedPath = directory+'merged.csv'):
    csvs = glob(top)
    merged = ""
    for csv in csvs:
        merged += strip(csv) + '\n'
        #break # TODO: remove break
    open(mergedPath, 'w').write(merged)
#merge()

def printRow(path = os.getcwd() + '/CSV_fall_data/**/*.csv', n = 4):
    csvs = glob(top)
    merged = []
    for csv in csvs:
        with open(csv) as csv:
            content = csv.readlines()
        merged.append(content[n])
    return merged
a = printRow(n=500)
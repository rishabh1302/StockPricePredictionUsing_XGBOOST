import numpy as numpy
import pandas as pd
import pickle
from os.path import isfile
import numpy as np
from sklearn.preprocessing import PolynomialFeatures


def initRegularize(path,df):
    meta = {}
    if(isfile(path+'/data.meta')):
        with open(path+'/data.meta','rb') as metaFile:
            meta = pickle.load(metaFile)
    else:
        print("Meta file not found!")
        return

    feature = {}
    for i in range(1,len(df[0])):
        arr = []
        for j in range(0,len(df)):
            arr.append(df[j][i])
        temp = {}
        temp['Min'] = np.min(arr)
        temp['Max'] = np.max(arr)
        temp['Mean'] = np.mean(arr)
        feature[i]=temp
    meta['RegParam']=feature

    with open(path+'/data.meta','wb') as metaFile:
        pickle.dump(meta,metaFile)
            
            
    




def regularize(path,df):
    #TODO make a model which will load pickle
    #return the modified values
    meta ={}
    if(isfile(path+'/data.meta')):
        with open(path+'/data.meta','rb') as metaFile:
            meta = pickle.load(metaFile)
    feature = meta['RegParam']
    df1 = pd.DataFrame()
    
    for i in feature.keys():
        temp = feature[i]
        arr = []
        df1[0]=[1]*(len(df))
        for j in range(0,len(df)):
            arr.append((df[j][i]-temp['Mean'])/(temp['Max']-temp['Min']))
        df1[i]=arr

    
    return df1



        
    

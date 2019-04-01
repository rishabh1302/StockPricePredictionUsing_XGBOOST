import pickle
from os.path import isfile

import numpy as np
import pandas as pd
import csv
from statsmodels.tsa.arima_model import ARIMA

from Model.ARIMA import ARIMAPredict, ARIMARegressor, ARIMATrain
#Mode numbers 
#1 - Gradient Boosted Trees
#2 - ARIMA
#3 - ANN
from Model.GradientBoostedTrees import GBTPredict, GBTRegressor, GBTTrain
from Model.preprocessing import prepareData
from Model.Regularizer import regularize
from Model.formatScript import findRSI,findMFI,findEMA,findMACD,findSO

# from Model.ANN import *

#TODO create a method to access different types of classifier 

def customName(mode):
    if(mode == 1):
        name = "GBT"
    elif(mode == 2):
        name = "ARIMA"
    elif(mode == 3): 
        name = "ANN"
    return name

def createModel(path,mode):

    name = customName(mode)
    if(mode == 1):
        clf = GBTRegressor()
    elif(mode == 2):
        clf = ARIMARegressor()
    # elif(mode == 3):
    #     clf = ANNRegressor()
    with open(path+"/"+name+"regressor.p",'wb') as file:
        pickle.dump(clf,file)
    

def trainModel(path,mode,X_train,y_train):
    name = customName(mode)
    if (isfile(path+"/"+name+"regressor.p")):
        with open(path+"/"+name+"regressor.p",'rb') as file:
            clf = pickle.load(file)
    else:
        print("Regressor not found")
        return
    if(mode == 1):
        #Code for GBT
        GBTTrain(clf,X_train,y_train)
    elif(mode == 2):
        #Code for ARIMA
        clf = ARIMATrain(0,X_train)

    
    # elif(mode == 3):
    #     #code for ANN
    #     ANNTrain(clf,X_train,y_train) 

    with open(path+"/"+name+"regressor.p",'wb') as file:
        pickle.dump(clf,file)



def predictValues(path,mode,X_test):
    name = customName(mode)
    if (isfile(path+"/"+name+"regressor.p")):
        with open(path+"/"+name+"regressor.p",'rb') as file:
            clf = pickle.load(file)
    else: 
        print("Regressor not found")
        return
    #TODO predict values and return it
    if(mode == 1):
        #Code for GBT
        val = GBTPredict(clf,X_test)
    elif(mode == 2):
        #Code for ARIMA
        ARIMAPredict(clf)
    # elif(mode == 3):
    #     #code for ANN
    #     ANNPredict(clf,X_test)
    #TODO create and save pickle from graphs
    #TODO save the predicted values as a document
    #TODO calculate accuracy metrics and save it

    return val


def predictRealTime(path,mode,daysLength):
    name = customName(mode)
    if (isfile(path+"/"+name+"regressor.p")):
        with open(path+"/"+name+"regressor.p",'rb') as file:
            reg = pickle.load(file)
    df = pd.read_csv(path+'/Data.csv')
    df = df[-40:]
    df.dropna(inplace=True)
    df.reset_index(inplace=True)
    try:
        df.drop(columns=['Unnamed: 0'],inplace=True)
        df.drop(columns=['index'],inplace=True)
    except:
        pass
    

    for i in range(0,daysLength):
        print("Day",i+1 , end = "  ")
        data = prepareData(df[-1:],1)
        X_lastRow = regularize(path,data)
        X_lastRow.columns=['0 ', '1 ', '2 ', '3 ', '4 ', '5 ', '6 ', '7 ', '8 ', '9 ', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20']
        pred = pd.DataFrame([[np.NaN]*len(df.columns)],columns=df.columns)

        pred['Diff'][0] = np.float64(reg.predict(X_lastRow))
        pred['Low'][0], pred['High'][0]  = predictLowAndHigh(df)
        pred['Volume'][0] = predictVolume(df)
        pred['Open'][0] = np.float64(df['Close'][-1:])
        pred['Close'][0] = pred['Open']+pred['Diff']
        print(pred['Close'][0])
        
        df = df.append(pred)
        df.reset_index(inplace=True)
        df.drop(columns=['index'],inplace=True)

        findRSI(df)
        findMFI(df)
        findEMA('EMA',df['Close'],df)
        findSO(df)
        findMACD(df)

    #post processing of data
    predValues = df[-daysLength*2:]
    predValues.reset_index(inplace = True)
    predValues = predValues.drop(columns=['index'])
    with open(path+'/PredictedValues.csv','w') as csvFile:
        fieldnames = predValues.columns.tolist()
        writer = csv.DictWriter(csvFile, fieldnames=fieldnames)
        writer.writeheader()
        
        for i in range (0,len(predValues)):
            row = {}
            for j in predValues.columns:
                rowKey = j
                rowValue = predValues[j][i]
                row[rowKey]=rowValue
            writer.writerow(row)

        

def predictLowAndHigh(df):
    rsi = np.float64(df['RSI'][-1:])
    openVal = np.float64(df['Open'][-1:])
    diff = np.float64(df['Diff'][-1:])
    predRange = np.float64(df['High'][-1:] - df['Low'][-1:])
    low = (100 * openVal - 100 * predRange + rsi * predRange) / 100
    if(diff<0):
        low = low + diff
        high = low + predRange
    else:
        high = low + predRange + diff
    return low,high

def predictVolume(df):
    volList = df['Volume'][-10:].tolist()
    diff = df['Diff'][-10:].tolist()

    volList,diff = col2sort(volList,diff)
    val = df['Diff'][-1:]
    val = np.float64(val)
    index = 0
    for i in range(0,len(volList)):
        if(val < diff[i]):
            index = i
            break
    return volList[index]
    
        
    
def col2sort(a,b):
    c = []
    d = []
    while (len(a)!=0):
        min = 0
        for j in range(0,len(a)):
            if(a[j]<a[min]):
                min = j
        c.append(a[min])
        d.append(b[min])
        del a[min]
        del b[min]
    return c,d

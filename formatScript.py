#import libraries
import numpy as np
import pandas as pd
import sys
import os
#import data from csv fill

#TODO make individual functions for each


def findRSI(df,rsiInternalLength = 14):
    #Feature 1 : RSI (Relative Strength Index)
    #RSI computes the relative strength index of a stock
    #Relative Strength (RS)= Avg of x up days/ Avg of x down days
    #RSI = 100-100/(1+RS)
    #Standard time period to calculate RSI is 14 days
    temp = [np.NAN]*rsiInternalLength
    for i in range(rsiInternalLength,len(df)):
        upcount = 0
        downcount = 0
        upsum = 0
        downsum = 0 
        for j in range(0,rsiInternalLength):
            if(df['Diff'][i-j]<0):
                downcount=downcount+1
                downsum = downsum + df['Close'][i-j]
            else:
                upcount=upcount+1
                upsum = upsum + df['Close'][i-j]
        try:
            rsUP = upsum/upcount
            rsDW = downsum/downcount
            rs = np.float64(100)-(np.float64(100)/(np.float64(1)+rsUP/rsDW))
            temp.append(rs)
        except:
            temp.append(np.NAN)
    #df.drop(columns='Diff',inplace=True)
    df['RSI'] = temp

def findMFI(df,mfiInternalLength = 14):
    #Feature 2 : Money Flow Index (MFI)
    #The Money Flow Index (MFI) is an oscillator that uses both price and volume to measure buying and selling pressure. 
    #Typical Price = (High + Low + Close)/3
    #Raw Money Flow = Typical Price x Volume
    #Money Flow Ratio = (14-period Positive Money Flow)/(14-period Negative Money Flow)
    #Money Flow Index = 100 - 100/(1 + Money Flow Ratio)
    #1 - High, 2 - Low, 3 - Close

    typicalPriceList = []
    rawMoneyFlowList = []

    for i in range(0,len(df)):
        tempTypical = (df['High'][i]+df['Low'][i]+df['Close'][i])/np.float64(3)
        typicalPriceList.append(tempTypical)
        rawMoneyFlowList.append(tempTypical * df['Volume'][i])
    df['Typical Price'] = typicalPriceList
    df['MF'] = rawMoneyFlowList
    mfiList = [np.NAN]*mfiInternalLength
    for i in range(mfiInternalLength,len(df)):
        pos = 0
        neg = 0
        possum = 0
        negsum = 0 
        for j in range(0,mfiInternalLength):
            if(df['Diff'][i-j]<0):
                neg=neg+1
                negsum = negsum + df['MF'][i-j]
            else:
                pos=pos+1
                possum = possum + df['MF'][i-j]
        try:
            mrUP = possum/pos
            mrDW = negsum/neg
            rs = np.float64(100)-(np.float64(100)/(np.float64(1)+mrUP/mrDW))
            mfiList.append(rs)
        except:
            mfiList.append(np.NAN)
    df['MFI'] = mfiList

def findEMA(finalName,feature,df,TimeInterval = 10):
    #Feature 3 : Exponential Moving Average (EMA)
    #Moving averages smooth the price data to form a trend following indicator.
    #Despite this lag, moving averages help smooth price action and filter out the noise.
    #Exponential moving averages (EMAs) reduce the lag by applying more weight to recent prices.
    #Initial SMA: 10-period sum / 10 
    #Multiplier: (2 / (Time periods + 1) ) = (2 / (10 + 1) ) = 0.1818 (18.18%)
    #EMA: {Close - EMA(previous day)} x multiplier + EMA(previous day). 
        emaMultiplier = 2/(TimeInterval+1)
        EMAlist = [np.NAN]*(TimeInterval-1)
        for i in range(TimeInterval-1,len(df)):
            initialEMA = np.sum(feature[i-TimeInterval+1:i+1])
            #print(initialEMA)

            #initialEMA = 0
            #for j in range(0,TimeInterval):
                #initialEMA = initialEMA + df['Close'][i-j]
            EMA = [initialEMA]
            for j in range(0,TimeInterval):
                tempEMA = (feature[i-(TimeInterval-j)+1]-EMA[-1])*emaMultiplier + EMA[-1]
                EMA.append(tempEMA)
                
            EMAlist.append(EMA[-1])
            #print(EMA)
        df[finalName] = EMAlist


def findSO(df,soTimeInterval = 7):
    #Feature 4 : Stocastic oscillator
    #Stochastic Oscillator is a momentum indicator that shows the location of the close relative to the 
    #high-low range over a set number of periods.
    #Default time peroid is 14 days but 7 days is used here
    #SO = (Current Close - Lowest Low)/(Highest High - Lowest Low) * 100

    soList = [np.NAN]*6
    for i in range(soTimeInterval-1,len(df)):   
        close = df['Close'][i]
        high=[]
        low=[]
        for j in range(0,soTimeInterval):
            high.append(df['High'][i-(soTimeInterval-j)+1])
            low.append(df['Low'][i-(soTimeInterval-j)+1])
        high = np.max(high)
        low = np.min(low)
        tempSO = (close-low)/(high-low)
        soList.append(tempSO)
    df['SO'] = soList

def findMACD(df):
    #Feature 5 : Moving Average Convergence/ Divergence
    #MACD Line: (12-day EMA - 26-day EMA)
    #Signal Line: 9-day EMA of MACD Line
    #MACD Histogram: MACD Line - Signal Line
    findEMA('EMA12',df['Close'],df,TimeInterval= 12)
    findEMA('EMA26',df['Close'],df,TimeInterval=26)
    df['MACD'] = df['EMA12']-df['EMA26']
    findEMA('Signal Line',df['MACD'],df,TimeInterval=9)





def formatData(folderPath,rawPath,outputPath):
    df = pd.read_csv(folderPath+rawPath)
    df.columns = ['Date','Open','High','Low','Close','Volume','Adjusted']

    df['Diff'] = df['Close'] - df['Close'].shift(+1)

    findRSI(df)
    findMFI(df)
    findEMA('EMA',df['Close'],df)
    findSO(df)
    findMACD(df)

    df.to_csv(folderPath+outputPath)



def formatHelper():
    dataPath = "./Data/"
    if(len(sys.argv[1:])==0):
        args = args = os.listdir(dataPath)
    else:
        args = sys.argv[1:]
    for i in args:
        rawFilePath = dataPath+i
        print("Started ",i,"   ")
        formatData(rawFilePath,"/Raw.csv","/Data.csv")



if __name__ == '__main__':
    formatHelper()
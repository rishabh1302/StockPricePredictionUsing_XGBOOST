from Model.ModelIntermediate import predictRealTime,trainModel
import os
import numpy as np
import pandas as pd
from Model.preprocessing import prepareData
from Model.Regularizer import regularize,initRegularize
from Model.ModelIntermediate import createModel


def realTimepred():

    daysPred = 7
    
    args = os.listdir("./Data/")
    for i in args:
        print(i)
        df = pd.read_csv("./Data/"+i+"/Data.csv")
        df.dropna(inplace=True)
        # df.reset_index(inplace=True)
        df.reset_index(inplace=True)
        try:
            df.drop(columns=['Unnamed: 0'],inplace=True)
            df.drop(columns=['index'],inplace=True)
        except:
            pass
	
        y = df['Diff']
        df = prepareData(df,1)
        initRegularize("./Data/"+i,df)
        df1 = regularize('./Data/'+i,df)
        
        createModel("./Data/"+i,1)
        trainModel("./Data/"+i,1,df1,y)


        predictRealTime("./Data/"+i,1,daysPred)
        

if __name__ == '__main__':
    realTimepred()


import os
import pandas as pd
import pickle
def populateData():
    df = pd.read_csv("./Companies.txt")
    if not(os.path.isdir('./Data')):
        os.mkdir('./Data')

    for i in df.index:
        folderName = df['Code'][i].replace('.','_')
        if not (os.path.isdir('./Data/'+folderName)):
            os.mkdir('./Data/'+folderName)
        if(os.path.isfile('./Data/'+folderName+'/data.meta')):
            with open('./Data/'+folderName+'/data.meta','rb') as metaFile:
                obj = pickle.load(metaFile)
        else:
            obj = {}
        obj['Code'] = df['Code'][i]
        obj['Name'] = df['Name'][i]
        obj['Type'] = df['Type'][i]
        obj['Capilatization'] = df['Cap'][i]
        with open('./Data/'+folderName+'/data.meta','wb') as openfile:
            pickle.dump(obj,openfile)
    # updateRawData()

def updateRawData():
    os.system('Rscript Scripts/GetCleanData.R')
    # os.system('python Model/formatScript.py')

def main():
    populateData()

if __name__ == '__main__':
    main()
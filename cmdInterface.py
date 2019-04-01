import os
from addCompany import addTheCompany
from Scripts.createMeta import populateData, updateRawData
from Model.formatScript import formatHelper
from RealTimePredict import realTimepred
from Model.PostPred import postPred


def main():
    print('Menu')
    print('1. Add company')
    print("2. Fetch Data")
    print("3. Clean Data")
    print("4. Run real time prediction")
    print("5. Exit")

    choice = int(input("Enter your choice:"))
    if(choice==1):
        addTheCompany()
    elif(choice==2):
        populateData()
        updateRawData()
    elif(choice==3):
        formatHelper()
    elif(choice==4):
        realTimepred()
        postPred()
    elif(choice==5):
        quit()
    elif(choice==10):
        populateData()
        updateRawData()
        formatHelper()
        realTimepred()
        postPred()

    else:
        print("Invalid option")

if __name__ == '__main__':
    while(True):
        main()
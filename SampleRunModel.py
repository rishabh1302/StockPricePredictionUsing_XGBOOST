
import numpy as np		
import pandas as pd
import os
from matplotlib import pyplot as plt
from sklearn.preprocessing import PolynomialFeatures
from Model.ModelIntermediate import createModel,predictValues,trainModel
from Model.Regularizer import regularize,initRegularize
from Model.preprocessing import prepareData


predictRange = 10

def sampleModel(predictqiRange,companyName,mode):
	print(predictRange,companyName)
	df = pd.read_csv("./Data/"+companyName+"/Data.csv")
	df.dropna(inplace=True)
	# df.reset_index(inplace=True)
	df.reset_index(inplace=True)
	try:
		df.drop(columns=['Unnamed: 0'],inplace=True)
		df.drop(columns=['index'],inplace=True)
	except:
		pass
	myindex = df.columns


	y = df['Diff']
	X_train = df[:-predictRange]
	y_train = y[:-predictRange]
	X_test = df[-predictRange:]
	# y_test = y[-predictRange:]
	
	df1 = prepareData(X_train,mode)
	df_test = prepareData(X_test,mode)

	initRegularize("./Data/"+companyName,df1)
	df1 = regularize("./Data/"+companyName,df1)
	df_test = regularize("./Data/"+companyName,df_test)

	# Training
	createModel("./Data/"+companyName,mode)
	trainModel("./Data/"+companyName,mode,df1,y_train)
	yPredicted = predictValues("./Data/"+companyName,mode,df_test)

	# print(yPredicted)
	# Finds the Correct ClosePrices

	acutalClose = [np.NAN]
	predictedClose = [np.NAN]
	pro = len(df)-predictRange
	for i in range(1,len(df)):
	    tempAcutal = df[myindex[-1]][i-1]+df['Diff'][i]
	    acutalClose.append(tempAcutal)
	    if(i>=pro):
	        
	        tempPre = predictedClose[i-1]+yPredicted[i-pro]
	    else:
	        tempPre = df[myindex[-1]][i-1]+df['Diff'][i]
	    predictedClose.append(tempPre)


	#plot Data
	plt.close()
	plt.plot(df['Date'][-predictRange*2:], acutalClose[-predictRange*2:], color='navy', label='Actual')

	plt.plot(df['Date'][-predictRange*2:], predictedClose[-predictRange*2:], color='darkorange',  label='Predicted')

	plt.xlabel('Date')
	plt.ylabel('Close')
	plt.title(companyName[:-17])
	plt.legend()
	# fig.savefig("./Data/"+companyName+"/Figure.png")
	
	# if(mode==1):
	# 	plt.savefig("./Data/"+companyName+"/GBTExample.png")
	# elif(mode==2):
	# 	plt.savefig("./Data/"+companyName+"/ARIMAExample.png")
	plt.close()
	

def main():
	args = os.listdir("./Data/")
	for i in args:
		sampleModel(predictRange,i,1)

if __name__ == '__main__':
	main()
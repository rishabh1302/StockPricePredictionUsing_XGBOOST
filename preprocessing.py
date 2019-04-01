#TODO make functions for each model.
#Where in the data is loaded and modelled 
#accordingly for different models.
from sklearn.preprocessing import PolynomialFeatures

def prepareData(df,mode):
    if(mode==1):
        df = prepareGBT(df)
    elif(mode==2):
        df = prepareARIMA(df)
    # elif(mode==3):
    #     df = prepareANN(df)
    return df

def prepareGBT(df):
    
    df = df[['RSI','MACD','EMA','MFI','SO']]
    poly = PolynomialFeatures(degree=2)
    df1 = poly.fit_transform(df)
    return df1

def prepareARIMA(df):
    df.index = df['Date']
    df = df['Close']
    print(df)
    return df

def prepareANN(df):
    pass


#TODO Return a data frame after mode
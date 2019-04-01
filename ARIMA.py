from statsmodels.tsa.arima_model import ARIMA



def ARIMARegressor():
    return {0:1}

def ARIMATrain(clf,X_train):
    clf = ARIMA(X_train,order = (5,2,3))
    clf_fit = clf.fit(disp= 0)
    return clf_fit

def ARIMAPredict(clf):
    val = clf.forecast(steps = 7)
    return val[0]
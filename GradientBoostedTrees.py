import xgboost as xgb



def GBTRegressor():
    clf  = xgb.XGBRegressor()
    return clf

def GBTTrain(clf,X_train,y_train):
    clf.fit(X_train,y_train)

def GBTPredict(clf,X_test):
    val = clf.predict(X_test)
    return val

#!/usr/bin/env python
# coding: utf-8

# In[702]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.arima_model import ARIMA
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.model_selection import train_test_split
import datetime
from xgboost import XGBRegressor
import warnings
warnings.filterwarnings("ignore")





def downloadHistory(startDate = '2019-01-01'):
    daterange = [d.strftime('%Y-%m-%d') for d in pd.date_range(startDate,str(pd.datetime.today().date()-datetime.timedelta(1)))]
    if daterange:
        result = pd.DataFrame(columns=daterange)
        for d in daterange:
            df = pd.read_html('https://www.xe.com/currencytables/?from=USD&date={}'.format(d))[0]
            result[d] = df['Units per USD']
        result.index = df.iloc[:,0]
        result.index.name = 'Code'
        return result

def initialize():
    result = downloadHistory()
    result.to_excel('ExrateHis.xlsx')
    return result


#Update
def updateHistoy():
    try:
        old = pd.read_excel('./forexer/ExrateHis.xlsx',index_col=0)
    except FileNotFoundError as e:
        return initialize()

    nextDay = str((pd.datetime.strptime(old.columns[-1],'%Y-%m-%d')+datetime.timedelta(1)).date())
    new = downloadHistory(nextDay)
    if new and len(new):
        result = pd.concat([old,new],axis=1)
        result.to_excel('./forexer/ExrateHis.xlsx')
        return result
    else:
        return old

def dataPrepare(country):
    for i in range(2014,2019):
        X['acccountBalance'+str(i)] = account_balance.at[country,i]
        X['inflationRate'+str(i)] = inflation_rate.at[country,i]
    return X





def xgb(X_train,y_train):
    X_train = X_train.dropna(axis=1)
    predictions=[]
    y_train.index = pd.date_range(y_train.index[0],y_train.index[-1])
    X_train.index = pd.date_range(X_train.index[0],X_train.index[-1])
    for i in range(10):
        
        xgbm = XGBRegressor()
        xgbm.fit(X_train.dropna(axis=1),y_train)
        history = y_train[-10:].append(X_train.iloc[-1][10:])
        history = pd.DataFrame(y_train[-10:].append(X_train.iloc[-1][10:])).T
        history.columns = X_train.columns
        predict = xgbm.predict(history)
        y_train.loc[y_train.index[-1]+datetime.timedelta(1)]=predict[0]
        X_train.loc[X_train.index[-1]+datetime.timedelta(1)]=history.values[0]
        predictions.append(predict[0])
    return (predictions)





def pairPredict(pairString):
    codes = pairString.split('/')
    toDay = str((pd.datetime.today().date()))
    lastDay = str((pd.datetime.today().date()+datetime.timedelta(9)))
    date_range = pd.date_range(toDay,lastDay)
    plt.title('pairString')
    return (np.array(predictDict[codes[0]])/np.array(predictDict[codes[1]]))






#Data loading
account_balance = pd.read_excel('./forexer/cleaned balance.xlsx')
inflation_rate = pd.read_excel('./forexer/cleaned ir.xlsx')
real_interenst_rate = pd.read_excel('./forexer/cleaned rate.xlsx')
account_balance = (account_balance.set_index(['Country Name','Year'])).unstack()
inflation_rate = (inflation_rate.set_index(['Country Name','Year'])).unstack()
real_interenst_rate = (real_interenst_rate.set_index(['Country Name','Year'])).unstack()
account_balance.columns = range(1995,2019)
inflation_rate.columns = range(1995,2019)
real_interenst_rate.columns = range(1995,2019)
account_balance = account_balance.diff()/account_balance.shift(1)
inflation_rate = inflation_rate.diff()
real_interenst_rate = real_interenst_rate.diff()



result = updateHistoy()
base = result.loc[['EUR','JPY','GBP','CHF','CAD','AUD']].copy()
base = base.T
base.index.name = 'Date'
X_raw = pd.concat([base.shift(-i).rename(columns={col:col+str(i) for col in base.columns}) for i in range(-10,0,1)],axis=1)
codedict={'EUR':'Euro area','JPY':'Japan','GBP':'United Kingdom',
          'CHF':'Switzerland','CAD':'Canada','AUD':'Australia'}
predictDict={}
for code in codedict:
    X = X_raw[[code+'-'+str(i) for i in range(10,0,-1)]][10:].copy()
    y = base[code][10:].copy()
    X = dataPrepare(codedict[code])
    predictDict[code] = xgb(X.copy(),y.copy())

predictDict['USD'] = [1 for i in range(10)]


if __name__ == "__main__":
    pairPredict('EUR/JPY')
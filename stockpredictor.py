# -*- coding: utf-8 -*-
"""StockPredictor

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/11PVoJcXXmOXOFr3KujhCIyCBAP9RXMtu

## **Importing Various Necessary Libraries**
"""

# Commented out IPython magic to ensure Python compatibility.
import warnings
warnings.filterwarnings('ignore')

# data wrangling & pre-processing
import pandas as pd
import numpy as np

# data visualization
import matplotlib.pyplot as plt
# %matplotlib inline
import seaborn as sns

from sklearn.model_selection import train_test_split


from scipy import stats

"""# **Importing Google Stock Price Data Set**
[Google Stock Price Data Set](https://finance.yahoo.com/quote/GOOG/history/?guccounter=1&guce_referrer=aHR0cHM6Ly93d3cuZ29vZ2xlLmNvbS8&guce_referrer_sig=AQAAALtRm22kpTDwOMnN2b_Z8UAzi0H0F8PtjTd8SyATYlfO7uDhkPnEGrtU1cAqA0rpceRou9nh8dHMUHh_LaXrZDCmUPo_6GkMDI9FaPuoz6OA5iYo-9jWkHxwP4uTFKRVOaOxgAeuy1OhppqrYv67lylGDCgcVwpST6tHFHkS90Uw)
"""

from google.colab import files
uploaded = files.upload()

"""# **Head and Tail of GOOGLE Stock Price Data Set**"""

pd.read_csv("GOOG1.csv")

data = pd.read_csv("GOOG1.csv")

"""## **Various Information regarding the attributes present in the Data Set** """

data.info()

"""# **Importing yfinance package for Exploratory Data Analysis**"""

!pip install yfinance
import yfinance as yf

goog = yf.download('data')

"""# **EXPLORATORY DATA ANALYSIS**
***>Stock Price Trend from August-2018 to August-2019***



"""

data['Open'].plot(label = 'Google', figsize = (15,7))
plt.title('Stock Prices')
plt.xlabel('Time')
plt.ylabel('Stock Price')
plt.legend()

"""***>Volume of Stock Traded from August-2018 to August-2019***"""

data['Volume'].plot(label = 'Google', figsize = (15,7))
plt.title('Volume of Stock traded')
plt.xlabel('Time')
plt.ylabel('Volume')
plt.legend()

"""***>Market Capitalization of Google Stock***"""

data['MarktCap'] = data['Open'] * data['Volume']
data['MarktCap'].plot(label = 'Google', figsize = (15,7))
plt.title('Market Cap')
plt.xlabel('Time')
plt.ylabel('Capitalization')
plt.legend()

"""***>Percentage increase in stock value***

//This basically determines the volatility of a stock.
"""

data['returns'] = (data['Close']/data['Close'].shift(1)) -1
data['returns'].hist(bins = 100, label = 'Google', alpha = 0.5, figsize = (15,7))
plt.title('Stock Volatitlity')
plt.xlabel('Time')
plt.ylabel('Volatility')
plt.legend()

"""# **//End of Exploratory Data Analysis!**

# **Analysis of LSTM Model for Stock Price Prediction**:
"""

import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense,LSTM,Dropout
from google.colab import files
uploaded = files.upload()
data1 = pd.read_csv('trainData.csv') 
data1["Close"]=pd.to_numeric(data1.Close,errors='coerce') #turning the Close column to numeric
data1 = data1.dropna() #romeving the NA values
trainData = data1.iloc[:,4:5].values #selecting only the closing prices for training
sc = MinMaxScaler(feature_range=(0,1))
trainData = sc.fit_transform(trainData)
trainData.shape

X_train = []
y_train = []

for i in range (60,1149): #60 : timestep // 1149 : length of the data
    X_train.append(trainData[i-60:i,0]) 
    y_train.append(trainData[i,0])

X_train,y_train = np.array(X_train),np.array(y_train)

X_train = np.reshape(X_train,(X_train.shape[0],X_train.shape[1],1)) #adding the batch_size axis
X_train.shape

model = Sequential()

model.add(LSTM(units=100, return_sequences = True, input_shape =(X_train.shape[1],1)))
model.add(Dropout(0.2))

model.add(LSTM(units=100, return_sequences = True))
model.add(Dropout(0.2))

model.add(LSTM(units=100, return_sequences = True))
model.add(Dropout(0.2))

model.add(LSTM(units=100, return_sequences = False))
model.add(Dropout(0.2))

model.add(Dense(units =1))
model.compile(optimizer='adam',loss="mean_squared_error")

hist = model.fit(X_train, y_train, epochs = 20, batch_size = 32, verbose=2)

testData = pd.read_csv('GOOG1.csv') #importing the test data
testData["Close"]=pd.to_numeric(testData.Close,errors='coerce') #turning the close column to numerical type
testData = testData.dropna() #droping the NA values
testData = testData.iloc[:,4:5] #selecting the closing prices for testing
y_test = testData.iloc[60:,0:].values #selecting the labels 
#input array for the model
inputClosing = testData.iloc[:,0:].values 
inputClosing_scaled = sc.transform(inputClosing)
inputClosing_scaled.shape
X_test = []
length = len(testData)
timestep = 60
for i in range(timestep,length): #doing the same preivous preprocessing 
    X_test.append(inputClosing_scaled[i-timestep:i,0])
X_test = np.array(X_test)
X_test = np.reshape(X_test,(X_test.shape[0],X_test.shape[1],1))
X_test.shape

y_pred = model.predict(X_test) #predicting the new values

predicted_price = sc.inverse_transform(y_pred) #inversing the scaling transformation for ploting

plt.plot(y_test, color = 'black', label = 'Actual Stock Price')
plt.plot(predicted_price, color = 'red', label = 'Predicted Stock Price')
plt.title('GOOGLE Stock Price Prediction - LSTM Model')
plt.xlabel('Time')
plt.ylabel('Stock Price')
plt.legend()
plt.show()

plt.plot(hist.history['loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train'], loc='upper left')
plt.show()

import math 
from sklearn.metrics import mean_squared_error
MSE_error1 = mean_squared_error(y_test, predicted_price)
print('Testing Mean Squared Error is {}'.format(MSE_error1))
print('The Root Mean Squared Error is:')
print(math.sqrt(MSE_error1))

"""# **Analysis of BI-LSTM Model for Stock Price Prediction**"""

import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense,LSTM,Dropout
from google.colab import files
uploaded = files.upload()
data1 = pd.read_csv('trainData.csv') 
data1["Close"]=pd.to_numeric(data1.Close,errors='coerce') #turning the Close column to numeric
data1 = data1.dropna() #romeving the NA values
trainData = data1.iloc[:,4:5].values #selecting only the closing prices for training
sc = MinMaxScaler(feature_range=(0,1))
trainData = sc.fit_transform(trainData)
trainData.shape

X_train = []
y_train = []

for i in range (60,1149): #60 : timestep // 1149 : length of the data
    X_train.append(trainData[i-60:i,0]) 
    y_train.append(trainData[i,0])

X_train,y_train = np.array(X_train),np.array(y_train)

X_train = np.reshape(X_train,(X_train.shape[0],X_train.shape[1],1)) #adding the batch_size axis
X_train.shape

from keras.layers import Bidirectional
model = Sequential()

model.add(Bidirectional(LSTM(units=100, return_sequences = True, input_shape =(X_train.shape[1],1))))
model.add(Dropout(0.2))

model.add(Bidirectional(LSTM(units=100, return_sequences = True)))
model.add(Dropout(0.2))

model.add(Bidirectional(LSTM(units=100, return_sequences = True)))
model.add(Dropout(0.2))

model.add(Bidirectional(LSTM(units=100, return_sequences = False)))
model.add(Dropout(0.2))

model.add(Dense(units =1))
model.compile(optimizer='adam',loss="mean_squared_error")

hist = model.fit(X_train, y_train, epochs = 20, batch_size = 32, verbose=2)

testData = pd.read_csv('GOOG1.csv') #importing the test data
testData["Close"]=pd.to_numeric(testData.Close,errors='coerce') #turning the close column to numerical type
testData = testData.dropna() #droping the NA values
testData = testData.iloc[:,4:5] #selecting the closing prices for testing
y_test = testData.iloc[60:,0:].values #selecting the labels 
#input array for the model
inputClosing = testData.iloc[:,0:].values 
inputClosing_scaled = sc.transform(inputClosing)
inputClosing_scaled.shape
X_test = []
length = len(testData)
timestep = 60
for i in range(timestep,length): #doing the same preivous preprocessing 
    X_test.append(inputClosing_scaled[i-timestep:i,0])
X_test = np.array(X_test)
X_test = np.reshape(X_test,(X_test.shape[0],X_test.shape[1],1))
X_test.shape

y_pred = model.predict(X_test) #predicting the new values

predicted_price = sc.inverse_transform(y_pred) #inversing the scaling transformation for ploting

plt.plot(y_test, color = 'black', label = 'Actual Stock Price')
plt.plot(predicted_price, color = 'red', label = 'Predicted Stock Price')
plt.title('GOOGLE Stock Price Prediction - BI-LSTM Model')
plt.xlabel('Time')
plt.ylabel('Stock Price')
plt.legend()
plt.show()

plt.plot(hist.history['loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train'], loc='upper left')
plt.show()

from sklearn.metrics import mean_squared_error
import math 
MSE_error2 = mean_squared_error(y_test, predicted_price)
print('Testing Mean Squared Error is {}'.format(MSE_error2))
print('The Root Mean Squared Error is:')
print(math.sqrt(MSE_error2))

"""# **Analysis of ARIMA Model for Stock Price Predcition**"""

import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
from pandas.plotting import lag_plot
from pandas import datetime
from statsmodels.tsa.arima_model import ARIMA
from sklearn.metrics import mean_squared_error

from google.colab import files
uploaded = files.upload()

df = pd.read_csv("GOOG1.csv")
df.head(5)

train_data, test_data = df[0:int(len(df)*0.7)], df[int(len(df)*0.7):]
training_data = train_data['Close'].values
test_data = test_data['Close'].values
history = [x for x in training_data]
model_predictions = []
N_test_observations = len(test_data)
for time_point in range(N_test_observations):
    model = ARIMA(history, order=(4,1,0))
    model_fit = model.fit(disp=0)
    output = model_fit.forecast()
    yhat = output[0]
    model_predictions.append(yhat)
    true_test_value = test_data[time_point]
    history.append(true_test_value)

test_set_range = df[int(len(df)*0.7):].index
plt.plot(test_set_range, model_predictions, color='blue', marker='o',label='Predicted Price')
plt.plot(test_set_range, test_data, color='red', label='Actual Price')
plt.title('Google Stock Price')
plt.xlabel('Date')
plt.ylabel('Prices')
plt.legend()
plt.show()

import math
MSE_error3 = mean_squared_error(test_data, model_predictions)
print('Testing Mean Squared Error is {}'.format(MSE_error3))
print('The Root Mean Squared Error is:')
print(math.sqrt(MSE_error3))

import matplotlib.pyplot as plt
fig = plt.figure()
ax = fig.add_axes([0,0,1,1])
MODELS = ['LSTM', 'BI-LSTM', 'ARIMA']
RMSE = [77.96,39.44,24.02]
ax.bar(MODELS,RMSE)
plt.show()

"""# **FINAL CONCLUSION**: We see ARIMA (AutoRegressive Integrated Moving Average) having the least Root Mean Squared Error and has the best performance.
// ARIMA > BI-LSTM > LSTM (Accuracy)
"""
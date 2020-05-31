#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 31 12:55:10 2020

@author: Allie
"""

import pandas as pd  
import numpy as np  
import matplotlib.pyplot as plt  
import seaborn as seabornInstance 
from sklearn.model_selection import train_test_split 
from sklearn.linear_model import LinearRegression
from sklearn import metrics

data = pd.read_csv('/Users/Allie/Documents/Python/Summer Project/RealEstate.csv')

#Tells us rows and columns 
data.shape

#Telling us the types of the columns
data.dtypes

#Gives us descriptive stats
data.describe()

#Changing the strings so these columns become floats
#Probably a better way to do this. Ask Jane
data['sqft'] = data.sqft.str.replace(",", "")
data['price'] = data.price.str.replace(",", "")
data['price'] = data.price.str.replace("$", "")

data.sqft = pd.to_numeric(data.sqft)
data.price = pd.to_numeric(data.price)



#Example of a plot
##Sale price vs Sqft
#'o' menas it will produce a small circle
#This doesnt work yet
data.plot(x='sqft', y ='price', stlye='o')
plt.title("Price vs Sqft")
plt.xlabel("Sqft")
plt.ylabel("Price")
plt.show

##Drop NaN values found in sqft
data = data.dropna(subset = ['sqft'])



##This is just practice; SLR only 
#Below I am just using sqft vs price

X = data['sqft'].values.reshape(-1,1)
y = data['price'].values.reshape(-1,1)

##Splitting the data into a training and testing set
#Training set is just the set we use to build the model
#We will use 10% of the data to test, hence test_size = 0.1
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=0)

#training the model 
regressor = LinearRegression()  
regressor.fit(X_train, y_train) 

##Get intercept and slope
print(regressor.intercept_)
print(regressor.coef_)


#making predictions on the test data 
y_pred = regressor.predict(X_test)

#Compare actual vs fitted
df = pd.DataFrame({'Actual': y_test.flatten(), 'Predicted': y_pred.flatten()})
df


#%%

#Heads up this doesn't work
#I need to look into how this works with categorical variables 

##Now try a bit with MLR
##Same libraries still apply 
##Still using same data set 

data = pd.read_csv('/Users/Allie/Documents/Python/Summer Project/RealEstate.csv')
list(data.columns)
#Checking which columns have NaN
##data = data.isnull().any()
#Remove all null values 
##data = data.fillna(method="ffill")




data['sqft'] = data.sqft.str.replace(",", "")
data['price'] = data.price.str.replace(",", "")
data['price'] = data.price.str.replace("$", "")

data.sqft = pd.to_numeric(data.sqft)
data.price = pd.to_numeric(data.price)

##Divide into attributes and labels 
#Attributes are independent variables aka X aka predictor 
#Labels are dependent variables aka Y aka response
X = data[['listing id',
 'prop type',
 'bed',
 'bath',
 'sqft',
 'garage']].values
y = data['price'].values



##Splitting the data into a training and testing set
#Training set is just the set we use to build the model
#We will use 10% of the data to test, hence test_size = 0.1
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=0)

##Train the model 
regressor = LinearRegression()  
regressor.fit(X_train, y_train)


##See the coefs. 
coeff_df = pd.DataFrame(regressor.coef_, X.columns, columns=['Coefficient'])  
coeff_df


##Predict on test data
y_pred = regressor.predict(X_test)

##Observe vs fitted
df = pd.DataFrame({'Actual': y_test, 'Predicted': y_pred})
df1 = df.head(25)







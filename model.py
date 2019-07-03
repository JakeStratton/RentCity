from sklearn.model_selection import train_test_split
import numpy as np 
import pandas as pd 
from sklearn.preprocessing import StandardScaler
from sklearn import linear_model
from sklearn.ensemble import RandomForestRegressor
from sklearn.datasets import make_regression

#load data
df = pd.read_csv('cleaned_rentals_info.csv')
y = df['price']
X = df.drop('price', axis='columns')
feature_list = list(X.columns)

#create train test splits
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.2)

#scale the X data
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

#I should be building pipelines for each model, need
#to go back and do that when I pollish the project

#Lasso model
def lasso():
    clf = linear_model.Lasso()
    clf.fit(X_train_scaled, y_train)
    lasso_score = clf.score(X_test_scaled, y_test)
    print('lasso_score -', lasso_score)
    
    return None


#random forest model
def random_forest(max_depth=8, n_estimators=50):
    rf_regr = RandomForestRegressor(max_depth=max_depth, random_state=0, n_estimators=n_estimators)
    rf_regr.fit(X_train_scaled, y_train)
    print(rf_regr.feature_importances_)
    print(rf_regr.predict(X_train_scaled))
    print("R2 Score -", rf_regr.score(X_train_scaled, y_train))

    return rf_regr


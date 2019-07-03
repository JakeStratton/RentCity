from sklearn.model_selection import train_test_split
import numpy as np 
import pandas as pd 
from sklearn.preprocessing import StandardScaler
from sklearn import linear_model
from sklearn.ensemble import RandomForestRegressor
from sklearn.datasets import make_regression
import plotly.plotly as py
import plotly.graph_objs as go
import plotly

#load data
df = pd.read_csv('cleaned_rentals_info.csv')
df = df.drop('Unnamed: 0', axis='columns')
df_not_above_6k = df[df['price'] < 6000]

y = df['price']
X = df.drop('price', axis='columns')

y_no_6k = df_not_above_6k['price']
X_no_6k = df_not_above_6k.drop('price', axis='columns')

feature_list = list(X.columns)


#create train test splits
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.2)
X_no_6k_train, X_no_6k_test, y_no_6k_train, y_no_6k_test = train_test_split(X_no_6k, y_no_6k, test_size=.2)

#scale the X data
scaler = StandardScaler()
scaler_no_6k = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
X_no_6k_train_scaled = scaler_no_6k.fit_transform(X_no_6k_train)
X_no_6k_test_scaled = scaler_no_6k.transform(X_no_6k_test)

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
def random_forest():
    rf_regr = RandomForestRegressor(max_depth=48, random_state=0, n_estimators=200)
    rf_regr.fit(X_train_scaled, y_train)
    print(rf_regr.feature_importances_)
    print(rf_regr.predict(X_train_scaled))
    print("R2 Score -", rf_regr.score(X_test_scaled, y_test))

    return rf_regr


# Get numerical feature importances
def get_feature_importances():
    rf_regr = random_forest()
    importances = list(rf_regr.feature_importances_)
    # List of tuples with variable and importance
    feature_importances = [(feature, round(importance, 2)) for feature, importance in zip(feature_list, importances)]
    # Sort the feature importances by most important first
    feature_importances = sorted(feature_importances, key = lambda x: x[1], reverse = True)
    # Print out the feature and importances 
    [print('Variable: {:20} Importance: {}'.format(*pair)) for pair in feature_importances];
    df_feature_importances = pd.DataFrame(feature_importances) 

    return df_feature_importances

#get y_hat
def get_y_hat():
    rf_regr = random_forest()
    y_hat = rf_regr.predict(X_test_scaled)
    return y_hat
'''
#get y_hat_no_6k
def get_y_hat_no_6k():
    rf_regr_no_6k = random_forest_no_6k()
    y_hat_no_6k = rf_regr_no_6k.predict(X_no_6k_test_scaled)
    return y_hat_no_6k
'''
'''
#random forest model no high prices (this needs to be integrated with the other RF function)
def random_forest_no_6k():
    rf_regr_no_6k = RandomForestRegressor(max_depth=48, random_state=0, n_estimators=200)
    rf_regr_no_6k.fit(X_no_6k_train_scaled, y_no_6k_train)
    #print(rf_regr_no_6k.feature_importances_)
    #print(rf_regr_no_6k.predict(X_train_scaled))
    print("R2 Score -", rf_regr_no_6k.score(X_no_6k_test_scaled, y_no_6k_test))

    return rf_regr_no_6k
'''


# plots

#print a map of a tree in teh forest
def tree_map():
    rf_regr = random_forest()
    # Import tools needed for visualization
    from sklearn.tree import export_graphviz
    import pydot
    # Pull out one tree from the forest
    tree = rf_regr.estimators_[5]
    # Export the image to a dot file
    export_graphviz(tree, out_file = 'tree.dot', feature_names = feature_list, rounded = True, precision = 1)
    # Use dot file to create a graph
    (graph, ) = pydot.graph_from_dot_file('tree.dot')
    # Write graph to a png file
    graph.write_png('tree.png')

    return None

def plot_residuals():
    y_hat = get_y_hat()
    y = y_hat - y_test
    x = y_hat

    # Create a trace
    trace = go.Scatter(
        x = x,
        y = y,
        mode = 'markers'
    )

    data = [trace]

    layout = dict(title = 'Residuals',
            hovermode= 'closest',
            yaxis = dict(zeroline = False, title = 'Predicted Price'
            ),
            xaxis = dict(zeroline = False, title = 'Actual Price'),
            showlegend= True)

    fig = dict(data=data, layout=layout)

    # Plot
    plotly.offline.plot(fig, filename='rf_results.html')

#plot feature importances
def plot_feature_importances():
    df = get_feature_importances().head(10)
    data = [go.Bar(
            x = df[0],
            y = df[1]
    )]
    layout = dict(title = 'Feature Importance',
            hovermode= 'closest',
            yaxis = dict(zeroline = False, title = 'Importance'
            ),
            xaxis = dict(zeroline = False, title = 'Feature'),
            showlegend= True)
    fig = dict(data=data, layout=layout)

    # Plot 
    plotly.offline.plot(fig, filename='feature_importances.html')
    

'''
def plot_residuals_no_6k():
    y_hat_no_6k = get_y_hat_no_6k()
    y = y_hat_no_6k - y_no_6k_test
    x = y_hat_no_6k

    # Create a trace
    trace = go.Scatter(
        x = x,
        y = y,
        mode = 'markers'
    )

    data = [trace]

    layout = dict(title = 'Residuals',
            hovermode= 'closest',
            yaxis = dict(zeroline = False, title = 'Predicted Price'
            ),
            xaxis = dict(zeroline = False, title = 'Actual Price'),
            showlegend= True)

    fig = dict(data=data, layout=layout)

    # Plot and embed in ipython notebook!
    plotly.offline.plot(fig, filename='rf_results_no_6k.html')


'''
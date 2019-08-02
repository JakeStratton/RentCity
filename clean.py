import pandas as pd 
import numpy as np 
import ast
from sklearn.preprocessing import MultiLabelBinarizer
import matplotlib.pyplot as plt
import matplotlib
from scipy import stats
import plotly.graph_objs as go
import plotly.plotly as py
import plotly.tools as tls
import plotly.figure_factory as ff
import copy
import plotly
import plotly.graph_objs as go


matplotlib.style.use('seaborn')

# load data, but modify the amenities column so that it come in as a list, as opposed to a string
generic = lambda x: x.strip('[').strip(']').replace(',', '').replace("'", '').split()
conv = {'amenities': generic, 'hood': generic, 'boro': generic}
df = pd.read_csv('rentals_info.csv', converters=conv)

#only include rows that have a valid building id
df = df[np.isfinite(df['bldgid'])]      

#drop rows with no price
df = df.dropna(subset=['price'])

#drop rows with no num of bedrooms listed
df = df.dropna(subset=['bd'])

#fill missing hood values with area value (only applies to 
# roosevelt island apartments)
df['hood'] = df['hood'].fillna(df['area'])

#fill na sqft values with median sqft of 
# apartments of that same number of beds
for i in df['bd'].unique():
    df['sqft'][df['bd'] == i] = df['sqft'].fillna(df['sqft'][df['bd'] == i].mean())

#drop rows with 0 as sqft (I need to add this to step above to impute the correct values)
indexNames = df[df['sqft'] == 0].index
# Delete these row indexes from dataFrame
df = df.drop(indexNames)

# drop rows with '' as hood
indexNameshood = df[df['hood'] == ''].index
df = df.drop(indexNameshood)

#fill parking NaNs with 0, and parking trues with 1
df['park'][df['park'] == 'true'] = 1
df['park'] = df['park'].fillna(0)

#fill broker fee yes' with 1, and no's with 0
df['brokerfee'][df['brokerfee'] == 'yes'] = 1
df['brokerfee'][df['brokerfee'] == 'no'] = 0

#round off all floats
df = df.round()   

#change columns to integer
df['zip'] = pd.to_numeric(df['zip'], downcast='integer')
df['bd'] = pd.to_numeric(df['bd'], downcast='integer')
df['price'] = pd.to_numeric(df['price'], downcast='integer')
df['bldgid'] = pd.to_numeric(df['bldgid'], downcast='integer')
df['bd'] = pd.to_numeric(df['bd'], downcast='integer')
df['sqft'] = pd.to_numeric(df['sqft'], downcast='integer')

#fill amenties NaNs with empty list
df['amenities'] = df['amenities'].fillna('None')

#drop unneded columns
df = df.drop('listtp',  axis='columns')
df = df.drop('proptp',  axis='columns')
df = df.drop('tflag',  axis='columns')
df = df.drop('vers',  axis='columns')
df = df.drop('cnty',  axis='columns')
df = df.drop('city',  axis='columns')
df = df.drop('state',  axis='columns')
df = df.drop('env',  axis='columns')
df = df.drop('pis',  axis='columns')
df = df.drop('area', axis='columns')
df = df.drop('oh', axis='columns')
df = df.drop('sqftrange', axis='columns')
df = df.drop('Unnamed: 0', axis='columns')
df = df.drop('prange', axis='columns')
df = df.drop('brokerage', axis='columns')
df = df.drop('yrblt', axis='columns')
df = df.drop('aamgnrc1', axis='columns')

#Binarize the amenities, hood, and boro columns
mlb = MultiLabelBinarizer()
df = df.join(pd.DataFrame(mlb.fit_transform(df.pop('amenities')),
                          columns=mlb.classes_,
                          index=df.index))

df = df.join(pd.DataFrame(mlb.fit_transform(df['hood']),
                          columns=mlb.classes_,
                          index=df.index))

df = df.join(pd.DataFrame(mlb.fit_transform(df['boro']),
                          columns=mlb.classes_,
                          index=df.index))

#clean boro and hood columns (list to string)
df['boro'] = [','.join(map(str, l)) for l in df['boro']]
df['hood'] = [','.join(map(str, l)) for l in df['hood']]

# drop rows with '' as hood
indexNameshood = df[df['hood'] == ''].index
df = df.drop(indexNameshood) #js

#drop unneded binary columns (includes features that 
# are the same across the entire building, because building ID 
# accounts for that)
df = df.drop('nyc_evacuation_1', axis='columns')
df = df.drop('nyc_evacuation_2', axis='columns')
df = df.drop('nyc_evacuation_3', axis='columns')
df = df.drop('nyc_evacuation_4', axis='columns')
df = df.drop('nyc_evacuation_5', axis='columns')
df = df.drop('nyc_evacuation_6', axis='columns')
df = df.drop('nyc_evacuation_c', axis='columns')
df = df.drop('assigned_parking', axis='columns')
df = df.drop('bayfront', axis='columns')
df = df.drop('board_approval_required', axis='columns')
df = df.drop('central_ac', axis='columns')
df = df.drop('co_purchase', axis='columns')
df = df.drop('cold_storage', axis='columns')
df = df.drop('concierge', axis='columns')
df = df.drop('courtyard', axis='columns')
df = df.drop('deck', axis='columns')
df = df.drop('guarantor_ok', axis='columns')
df = df.drop('guarantors', axis='columns')
df = df.drop('land_lease', axis='columns')
df = df.drop('leed_registered', axis='columns')
df = df.drop('oceanfront', axis='columns')
df = df.drop('parents', axis='columns')
df = df.drop('pied_a_terre', axis='columns')
df = df.drop('waterview', axis='columns')
df = df.drop('waterfront', axis='columns')
df = df.drop('valet', axis='columns')
df = df.drop('valet_parking', axis='columns')
df = df.drop('smoke_free', axis='columns')
df = df.drop('bldgid', axis='columns')

#combine redundant columns
df['sublet'] = df[['sublet', 'sublets']].max(axis=1)
df = df.drop('sublets', axis='columns')
df['doorman'] = df[['doorman', 'full_time_doorman', 'part_time_doorman']].max(axis=1)
df = df.drop('part_time_doorman', axis='columns')
df = df.drop('full_time_doorman', axis='columns')
df['pets'] = df[['cats', 'dogs', 'pets']].max(axis=1)
df = df.drop('dogs', axis='columns')
df = df.drop('cats', axis='columns')
df['storage'] = df[['storage', 'storage_room']].max(axis=1)
df = df.drop('storage_room', axis='columns')
df['parking'] = df[['park', 'parking']].max(axis=1)
df = df.drop('park', axis='columns')

#reset index
df = df.reset_index()

#EDA

#get means by num of bedrooms
sqft_means = []
for i in df['bd'].unique():
    sqft_means.append((i, df['sqft'][df['bd'] == i].mean()))

#get stats before removing outliers
price_stats_out = df['price'].describe()
sqft_stats_out = df['sqft'].describe()
beds_stats_out = df['bd'].describe()

#identify price outliers, using z-score with a threshold of 3
z = np.abs(stats.zscore(df['price']))
threshold = 3 
outliers = np.where(z >= 3)
outliers = outliers[0].tolist()
df = df.drop(df.index[outliers])

#reset index
df = df.reset_index()

#create new clean df and remove text features and nuneeded columns
df_cleaned = df
df_cleaned = df_cleaned.drop('hood', axis='columns')
df_cleaned = df_cleaned.drop('boro', axis='columns')
df_cleaned = df_cleaned.drop('zip', axis='columns')
df_cleaned = df_cleaned.drop('index', axis='columns')
df_cleaned = df_cleaned.drop('level_0', axis='columns')

#save as clean csv
df_cleaned.to_csv('cleaned_rentals_info.csv')

#get stats after removing outliers
price_stats = df['price'].describe()
sqft_stats = df['sqft'].describe()
beds_stats = df['bd'].describe()

#make plots

# make price hist, less than 10k only
def price_hist_lessthan10k():
    ax = df['price'][df['price'] <= 10000].hist(bins=100, edgecolor='black')
    ax.set_xlabel('Rent')
    ax.set_ylabel('Apartments')
    ax.set_title('Prices of Available Apartments - Below $10k')
    plt.show()

def price_hist_morethan10k():
    ax = df['price'][df['price'] > 10000].hist(bins=100, edgecolor='black')    
    ax.set_xlabel('Rent')
    ax.set_ylabel('Apartments')
    ax.set_title('Prices of Available Apartments - Above $10k')
    plt.show()

def price_hist():
    ax = df['price'].hist(bins=100, edgecolor='black')    
    ax.set_xlabel('Rent')
    ax.set_ylabel('Apartments')
    ax.set_title('Prices of Available Apartments - No Outliers')
    plt.show()

def price_per_beds():
    df = pd.DataFrame(sqft_means) 
    ax = plt.bar(df[0],df[1])
    ax.xlabel('Bedrooms')
    ax.ylabel('Mean Price')
    ax.title('Mean Prices by Number of Bedrooms')
    plt.show()
    

def scatter_price_sqft_boro():
    boros = np.unique(df['boro'].values).tolist() 
    boros_code = {boros[k]: k for k in range(5)}
    color_vals = [boros_code[cl] for cl in df['boro']] 
    pl_colorscale=[[0.0, 'red'],
                [0.2, 'red'],
                [0.2, 'blue'],
                [0.4, 'blue'],
                [0.4, 'green'],
                [0.6, 'green'],
                [0.6, 'yellow'],
                [0.8, 'yellow'],
                [0.8, 'purple'],
                [1, 'purple']]
    text = [df.loc[k, 'bd'] for k in range(len(df))]
    trace1 = go.Splom(dimensions=[dict(label='sqft',
                                    values=df['sqft']),
                            dict(label='price',
                                    values=df['price'])],
                text=text,
                #default axes name assignment :
                #xaxes= ['x1','x2',  'x3'],
                #yaxes=  ['y1', 'y2', 'y3'], 
                marker=dict(color=color_vals,
                            size=7,
                            colorscale=pl_colorscale,
                            showscale=False,
                            line=dict(width=0.5,
                                        color='rgb(230,230,230)'))
                )

    #trace1['diagonal'].update(visible=False)
    #trace1['showupperhalf']=False

    axis = dict(showline=True,
            zeroline=False,
            gridcolor='#fff',
            ticklen=4)

    layout = go.Layout(
        title='Price vs Sqft',
        dragmode='select',
        width=900,
        height=900,
        autosize=True,
        hovermode='closest',
        plot_bgcolor='rgba(240,240,240, 0.95)',
        xaxis1=dict(axis),
        yaxis1=dict(axis)
    )

    fig1 = dict(data=[trace1], layout=layout)
    py.iplot(fig1, filename='splom_price_sqft_boro.html')


def price_sqft_scatter_boro_color():
        trace0 = go.Scatter(
        x = df['sqft'][df['boro'] == 'manhattan'],
        y = df['price'][df['boro'] == 'manhattan'],
        name = 'Manhattan',
        mode = 'markers',
        text = [df.loc[k, 'bd'] for k in range(len(df))],
        marker = dict(
                size = 10,
                color = 'green',
                line = dict(
                width = 2,
                color = 'rgb(0, 0, 0)'
                )
        )
        )

        trace1 = go.Scatter(
        x = df['sqft'][df['boro'] == 'brooklyn'],
        y = df['price'][df['boro'] == 'brooklyn'],
        name = 'Brooklyn',
        mode = 'markers',
        marker = dict(
                size = 10,
                color = 'blue',
                line = dict(
                width = 2,
                color = 'rgb(0, 0, 0)'
                )
        )
        )

        trace2 = go.Scatter(
        x = df['sqft'][df['boro'] == 'queens'],
        y = df['price'][df['boro'] == 'queens'],
        name = 'Queens',
        mode = 'markers',
        marker = dict(
                size = 10,
                color = 'red',
                line = dict(
                width = 2,
                color = 'rgb(0, 0, 0)'
                )
        )
        )

        trace3 = go.Scatter(
        x = df['sqft'][df['boro'] == 'bronx'],
        y = df['price'][df['boro'] == 'bronx'],
        name = 'Bronx',
        mode = 'markers',
        marker = dict(
                size = 10,
                color = 'yellow',
                line = dict(
                width = 2,
                color = 'rgb(0, 0, 0)'
                )
        )
        )

        trace4 = go.Scatter(
        x = df['sqft'][df['boro'] == 'staten-island'],
        y = df['price'][df['boro'] == 'staten-island'],
        name = 'Staten Island',
        mode = 'markers',
        marker = dict(
                size = 10,
                color = 'purple',
                line = dict(
                width = 2,
                color = 'rgb(0, 0, 0)'
                )
        )
        )

        data = [trace0, trace1, trace2, trace3, trace4]

        layout = dict(title = 'Price vs. Sqft',
                hovermode= 'closest',
                yaxis = dict(zeroline = False, title = 'Price'
                ),
                autosize=True,
                xaxis = dict(zeroline = False, title = 'sqft'),
                showlegend= True)

        fig = dict(data=data, layout=layout)
        py.iplot(fig, filename='scatter_price_sqft_color_boro.html')


def top_hoods_horz_bar():
        df_mean_price_hood = pd.DataFrame()
        df_mean_price_hood[['hood', 'price', 'sqft']] = df[['hood', 'price', 'sqft']]

        hoods = df['hood'].unique().tolist()  
        y = []
        x = []

        for hood in hoods:
                hood_price_mean = df_mean_price_hood['price'][df_mean_price_hood['hood'] == hood].mean()
                hood_sqft_mean = df_mean_price_hood['sqft'][df_mean_price_hood['hood'] == hood].mean()
                hood_mean = hood_price_mean / hood_sqft_mean
                hood_mean = np.round(hood_mean, decimals=2)
                y.append(hood_mean)
                x.append(hood)


        df_mean_price_hood = pd.DataFrame({'mean_price': y, 'hood': x})
        df_mean_price_hood = df_mean_price_hood.sort_values('mean_price', ascending=False).head(20)
        yy = df_mean_price_hood['mean_price'].tolist()
        xx = df_mean_price_hood['hood'].tolist()


        trace0 = go.Bar(
        x = df_mean_price_hood['mean_price'],
        y = df_mean_price_hood['hood'],
        marker=dict(
                color='rgba(50, 171, 96, 0.6)',
                line=dict(
                color='rgba(50, 171, 96, 1.0)',
                width=1),
        ),
        name='Price per Sqft',
        orientation='h',
        )

        layout = dict(
        title='Price Per Sqft by Neighborhood',
        yaxis=dict(
                showgrid=False,
                showline=False,
                showticklabels=True,
                domain=[0, 0.85],
        ),
        xaxis=dict(
                zeroline=False,
                showline=False,
                showticklabels=True,
                showgrid=True,
                title='Price per Sqft',
                domain=[0, 0.42],
        ),
        legend=dict(
                x=0.029,
                y=1.038,
                font=dict(
                size=10,
                ),
        ),
        margin=dict(
                l=150,
                r=20,
                t=70,
                b=70,
        ),
        paper_bgcolor='rgb(248, 248, 255)',
        plot_bgcolor='rgb(248, 248, 255)',
        )

        annotations = []

        y_s = np.round(yy, decimals=2)

        # Adding labels
        for yd, xd in zip(yy, xx):
                # labeling the bar 
                annotations.append(dict(xref='x1', yref='y1',
                                        y=xd, x=yd + 3,
                                        text = str('$' + str(yd)),
                                        font=dict(family='Arial', size=12,
                                                color='rgb(50, 171, 96)'),
                                        showarrow=False))
        '''# Source
        annotations.append(dict(xref='paper', yref='paper',
                                x=-0.2, y=-0.109,
                                text='                                                              www.streeteasy.com (Collected June 28-30 2019)',
                                font=dict(family='Arial', size=10,
                                        color='rgb(150,150,150)'),
                                showarrow=False))'''

        layout['annotations'] = annotations


        fig = go.Figure(data=[trace0], layout=layout)

        fig['layout'].update(layout)
        py.iplot(fig, filename='hood_horz_bar_price_ranked.html')


def boros_horz_bar():
        df_mean_price_boro = pd.DataFrame()
        df_mean_price_boro[['boro', 'price', 'sqft']] = df[['boro', 'price', 'sqft']]

        boros = df['boro'].unique().tolist()  
        y = []
        x = []

        for boro in boros:
                boro_price_mean = df_mean_price_boro['price'][df_mean_price_boro['boro'] == boro].mean()
                boro_sqft_mean = df_mean_price_boro['sqft'][df_mean_price_boro['boro'] == boro].mean()
                boro_mean = boro_price_mean / boro_sqft_mean
                boro_mean = np.round(boro_mean, decimals=2)
                y.append(boro_mean)
                x.append(boro)

        df_mean_price_boro = pd.DataFrame({'mean_price': y, 'boro': x})
        df_mean_price_boro = df_mean_price_boro.sort_values('mean_price', ascending=False).head(20)
        yy = df_mean_price_boro['mean_price'].tolist()
        xx = df_mean_price_boro['boro'].tolist()


        trace0 = go.Bar(
        x = df_mean_price_boro['mean_price'],
        y = df_mean_price_boro['boro'],
        marker=dict(
                color='rgba(50, 171, 96, 0.6)',
                line=dict(
                color='rgba(50, 171, 96, 1.0)',
                width=1),
        ),
        name='Price per Sqft',
        orientation='h',
        )

        layout = dict(
        title='Price per Sqft by Borough',
        yaxis=dict(
                showgrid=False,
                showline=False,
                showticklabels=True,
                domain=[0, 0.85],
        ),
        xaxis=dict(
                zeroline=False,
                showline=False,
                showticklabels=True,
                showgrid=True,
                title='Price per Sqft',
                domain=[0, 0.42],
        ),
        autosize=True,
        legend=dict(
                x=0.029,
                y=1.038,
                font=dict(
                size=10,
                ),
        ),
        margin=dict(
                l=150,
                r=20,
                t=70,
                b=70,
        ),
        paper_bgcolor='rgb(248, 248, 255)',
        plot_bgcolor='rgb(248, 248, 255)',
        )

        annotations = []

        y_s = np.round(yy, decimals=2)

        # Adding labels
        for yd, xd in zip(yy, xx):
                # labeling the bar 
                annotations.append(dict(xref='x1', yref='y1',
                                        y=xd, x=yd + 3,
                                        text = str('$' + str(yd)),
                                        font=dict(family='Arial', size=12,
                                                color='rgb(50, 171, 96)'),
                                        showarrow=False))
        '''# Source
        annotations.append(dict(xref='paper', yref='paper',
                                x=-0.2, y=-0.109,
                                text='                                                                  www.streeteasy.com (Collected June 28-30 2019)',
                                font=dict(family='Arial', size=10,
                                        color='rgb(150,150,150)'),
                                showarrow=False))'''

        layout['annotations'] = annotations

        fig = dict(data=[trace0], layout=layout)
        #fig = go.Figure(data=[trace0], layout=layout)

        fig['layout'].update(layout)
        py.iplot(fig, filename='boro_horz_bar_price_ranked.html')
        
                
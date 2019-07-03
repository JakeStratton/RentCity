import plotly.plotly as py
import plotly.graph_objs as go
from plotly import tools

import numpy as np

df_mean_price_hood = pd.DataFrame()
df_mean_price_hood[['hood', 'price']] = df[['hood', 'price']]
'''

df_mean_price_hood = df_mean_price_hood.reset_index()
df_mean_price_hood = df_mean_price_hood.drop('index', axis='columns')
'''

hoods = df['hood'].unique().tolist()  
y = []
x = []

for hood in hoods:
        hood_mean = df_mean_price_hood['price'][df_mean_price_hood['hood'] == hood].mean()
        hood_mean = np.round(hood_mean, decimals=0)
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
    name='Mean Price',
    orientation='h',
)

layout = dict(
    title='Mean Price by Neighborhood',
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
        title='Mean Price',
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
        l=100,
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
for yd, xd in zip(y_s, xx):
    # labeling the bar 
    annotations.append(dict(xref='x1', yref='y1',
                            y=xd, x=yd + 3,
                            text=str(yd),
                            font=dict(family='Arial', size=12,
                                      color='rgb(50, 171, 96)'),
                            showarrow=False))
# Source
annotations.append(dict(xref='paper', yref='paper',
                        x=-0.2, y=-0.109,
                        text='streeteast.com (Collected June 28-30 2019)',
                        font=dict(family='Arial', size=10,
                                  color='rgb(150,150,150)'),
                        showarrow=False))

layout['annotations'] = annotations


fig = go.Figure(data=[trace0], layout=layout)

fig['layout'].update(layout)
plotly.offline.plot(fig, filename='hood_horz_bar_price_ranked.html')


        
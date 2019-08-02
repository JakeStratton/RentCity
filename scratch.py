import plotly.plotly as py
import plotly.graph_objs as go
#
data = [go.Bar(
            x = df['0'],
            y = df[1]
    )]

py.iplot(data, filename='feature_importances')
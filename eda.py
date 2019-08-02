import plotly.graph_objs as go
import plotly.plotly as py
import plotly.tools as tls
import plotly.figure_factory as ff

import copy
import numpy as np
import pandas as pd


df_table = ff.create_table(df.head())
py.iplot(df_table, filename='iris-data-head')


df_no_binary['boro'] = df_no_binary['boro'].map(lambda x: x.lstrip('[').rstrip(']'))


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
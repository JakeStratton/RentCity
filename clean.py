import pandas as pd 
import numpy as np 


df = pd.read_csv('rentals_info.csv')

#only include rows that have a valid building id
df = df[np.isfinite(df['bldgid'])]

#change zip code to integer
df['zip'] = pd.to_numeric(df['zip'], downcast='integer')

#change beds to integer
df['bd'] = pd.to_numeric(df['bd'], downcast='integer')

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

#round off all floats
df = df.round()         

#change sqft to integer
df['sqft'] = pd.to_numeric(df['sqft'], downcast='integer')

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




#get means by num of bedrooms
sqft_means = []
for i in df['bd'].unique():
    sqft_means.append((i, df['sqft'][df['bd'] == i].mean()))

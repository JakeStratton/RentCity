import pandas as pd 
import numpy as np 


df = pd.read_csv('rentals_info.csv')

#only include rows that have a valid building id
df = df[np.isfinite(df['bldgid'])]

#change zip code to integer
df['zip'] = pd.to_numeric(df['zip'], downcast='integer')

#drop rows with no price
df = df.dropna(subset=['price'])


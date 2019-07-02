import pandas as pd 
import numpy as np 
import ast
from sklearn.preprocessing import MultiLabelBinarizer

# load data, but modify the amenities column so that it come in as a list, as opposed to a string
generic = lambda x: x.strip('[').strip(']').replace(',', '').replace("'", '').split()
conv = {'amenities': generic}
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

#fill parking NaNs with 0, and parking trues with 1
df['park'][df['park'] == 'true'] = 1
df['park'] = df['park'].fillna(0)

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

#Binarize the amenities column
mlb = MultiLabelBinarizer()
df = df.join(pd.DataFrame(mlb.fit_transform(df.pop('amenities')),
                          columns=mlb.classes_,
                          index=df.index))

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

#combine redundant columns
df['sublet'] = df[['sublet', 'sublets']].max(axis=1)
df = df.drop('sublets', axis='columns')
df = df.drop('sublet', axis='columns')
df['doorman'] = df[['doorman', 'full_time_doorman', 'part_time_doorman']].max(axis=1)
df = df.drop('doorman', axis='columns')
df = df.drop('part_time_doorman', axis='columns')
df = df.drop('full_time_doorman', axis='columns')
df['pets'] = df[['cats', 'dogs', 'pets']].max(axis=1)
df = df.drop('dogs', axis='columns')
df = df.drop('cats', axis='columns')
df = df.drop('pets', axis='columns')
df['storage'] = df[['storage', 'storage_room']].max(axis=1)
df = df.drop('storage', axis='columns')
df = df.drop('storage_room', axis='columns')

#get means by num of bedrooms
sqft_means = []
for i in df['bd'].unique():
    sqft_means.append((i, df['sqft'][df['bd'] == i].mean()))
import pandas as pd
# loading the data using pandas' read_json file.
data = pd.read_json('data/tops_fashion.json')
data = data.loc[~data['formatted_price'].isnull()]#this will remove data with no price
data =data.loc[~data['color'].isnull()]#remove data with no color
#print(sum(data.duplicated('title')))#tell about dubplicate  
from remove_duplicate import remove_dup1,remove_dup2   
data=remove_dup1(data)#removes adjacent sorted same title
data=remove_dup2(data)#this will take time approx half hour
data.to_pickle('pickels/clean data')
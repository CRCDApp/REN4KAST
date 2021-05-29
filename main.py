#from GeneralForecastHandler import get_forecasts_for_today
import pandas as pd
import dateutil.parser
#get_forecasts_for_today()
#tmppp= forecast.values.tolist()
from MongoDbController import insert_many_mongo,read_mongo
import dateutil.parser

def read_and_split_data(target_period_days=3,start_date="2019-07-01 01:00:00",days_to_test=1, exog_columns=['windspeed','GHI'],file_name='twoWeeks'):
  data = pd.read_csv('{}.csv'.format(file_name), index_col=0)
  data.index = pd.date_range(start=data.index[0], periods=len(data), freq='15Min')
  #rengeneration = pd.read_csv('/content/drive/My Drive/generationOnly.csv', index_col=0)
  #rengeneration.index = pd.date_range(start=data.index[0], periods=len(rengeneration), freq='15Min')
  #data['renewablespercentage'] = rengeneration["percentage"][:len(data)]

  #starting the data from the mentioned day
  data = data[data.index >= dateutil.parser.parse(start_date)]
  #only considering the target period of days, 24 hours per day and 4 observations per hour
  data = data.iloc[:int(target_period_days*24*4),:]
  #calculating number of test data 24 hours per day and 4 observations per hour
  test_size = days_to_test*24*4
  train_size = int(data.shape[0]-test_size)
  train,test = data.renewablespercentage[0:train_size], data.renewablespercentage[train_size:]
  # selecting defined columns for exog parameters
  exog_train,exog_test = data[0:train_size].iloc[:, [data.columns.get_loc(ex) for ex in exog_columns]], data[train_size:].iloc[:, [data.columns.get_loc(ex) for ex in exog_columns]]
  # old way
  #exog_train,exog_test = data[0:train_size].loc[:, exog_columns], data[train_size:].loc[:, exog_columns]
  return train,test,exog_train,exog_test,data

train, test, exog_train, exot_test, data = read_and_split_data(file_name='ultimate_data')
#print(train[:2])

df = train.reset_index()
#print(df[:2].to_dict("records"))
#print(insert_many_mongo(db="food", collection="fruit", insertList=[{ "name": "William", "address": "Central st 954"},{"name": "William", "address": "Park Lane 38" }]))
collection="rencollsectiondtesffttt132"
#insert_many_mongo(db="rentest", collection=collection, insertList=df[0:3].to_dict("records"))
# data_from_db= read_mongo(db="rentest", collection=collection, query={"index": {
#         "$gte": dateutil.parser.parse("2019-07-01 01:15:00")
#         #,"$lt": dateutil.parser.parse("2019-07-01 01:16:00")
#     }
# })

data_from_db=read_mongo(db="rentest", collection="renewables_percentagetest", query={}, sort=[('index', 1)])
print("here is data from db")
print(data_from_db)
df = pd.DataFrame(data_from_db)
#df.set_index("index",inplace=True)
print(df)
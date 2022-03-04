import pandas as pd
import pymongo


def _connect_mongo(host, port, username, password, db):
    """ A util for making a connection to mongo """
    conn = pymongo.MongoClient('mongodb://%s:%s/' % (host, port), username=username, password=password)
    return conn[db]


def read_mongo(db, collection, query={}, host='192.168.0.219', port=27017, username="root", password="rootpassword", no_id=True, sort=[], limit=9999999):
    """ Read from Mongo and Store into DataFrame """

    # Connect to MongoDB
    db = _connect_mongo(host=host, port=port, username=username, password=password, db=db)

    # Make a query to the specific DB and Collection
    cursor = db[collection].find(query).sort(sort).limit(limit)#.distinct("index")

    # Expand the cursor and construct the DataFrame
    df =  pd.DataFrame.from_records(cursor)
    aa= df.index.unique()
    print(aa)
    # Delete the _id
    #if no_id:
    #    del df['_id']

    return df

def insert_many_mongo(db, collection, insertList=[], host='192.168.0.219', port=27017, username="root", password="rootpassword", no_id=True, index_column="index"):
    """ Read from Mongo and Store into DataFrame """

    # Connect to MongoDB
    db = _connect_mongo(host=host, port=port, username=username, password=password, db=db)

    # Make a query to the specific DB and Collection
    cursor = db[collection].insert_many(insertList)

    # index column = unique, sort: Ascending (because of 1), indexing will be done in background
    print(db[collection].create_index([(index_column, 1)], unique=True, background=True))

    return cursor.inserted_ids


#print(read_mongo(db="food", collection="fruit", query={ "address": "Park Lane 38" }))
#print(read_mongo(db="food", collection="fruit", query={}))

#print(insert_many_mongo(db="food", collection="fruit", insertList=[{ "name": "William", "address": "Central st 954"},{"name": "William", "address": "Park Lane 38" }]))
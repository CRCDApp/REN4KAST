from pymongo import MongoClient

# ping host.docker.internal to get ip
client = MongoClient('mongodb://root:rootpassword@192.168.0.219:27017/food?authSource=admin')
# client = MongoClient(host="0.0.0.0",
#                      port=27017,
#                      username="root",
#                      password="rootpassword"
#                      )#,authSource="admin")
#client = MongoClient("mongodb://root:12%40rootpassword@127.0.0.1:27017/food",authSource="admin")
db = client['food']

result = db.fruit.find()
for document in result:
    print(document)
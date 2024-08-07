
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://adityachowdhri2:2be4cwEO83xNRiqA@webscraping.9rrm6xc.mongodb.net/?appName=WebScraping"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
def func():
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
        db_name = "WebScrappingInformation"
        db = client[db_name]

    # Specify the collection name
        collection_name = "websites"
        collection = db[collection_name]
        for doc in collection.find():
            print(doc)
    except Exception as e:
        print(e)

func()
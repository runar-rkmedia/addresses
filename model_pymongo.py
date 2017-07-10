"""pymongo setup."""
import os
from pymongo import MongoClient,GEO2D

url = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/testdb')
database = os.getenv('MONGO_ADRESS_DB', 'address_database')
client = MongoClient(url)
db = client[database]
collection = db.address_collection
collection.create_index([('loc', GEO2D)])

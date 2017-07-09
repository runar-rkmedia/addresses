"""pymongo setup."""
import os
from pymongo import MongoClient

url = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/testdb')
database = os.getenv('MONGO_ADRESS_DB', 'address_database')
client = MongoClient(url)
db = client[database]
collection = db.address_collection

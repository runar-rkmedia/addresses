"""pymongo setup."""

from pymongo import MongoClient
client = MongoClient()
db = client.address_database
collection = db.address_collection

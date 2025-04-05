from pymongo import MongoClient
from datetime import datetime
from typing import List, Dict

MONGO_URI = 'mongodb://localhost:27017/'
DATABASE_NAME = 'linkscribedb'
COLLECTION_NAME = 'searches'

class MongoDBHandler:
    def __init__(self, mongodb_uri= MONGO_URI, db_name= DATABASE_NAME, collection_name= COLLECTION_NAME):
        self.mongodb_uri = mongodb_uri
        self.db_name = db_name
        self.collection_name = collection_name
        self.client = None
        self.db = None
        self.collection = None
        self._connect_db()

    def _connect_db(self):
        try:
            self.client = MongoClient(self.mongodb_uri)
            self.client.admin.command('ping')
            self.db = self.client[self.db_name]
            self.collection = self.db[self.collection_name]
            print(f"Connected to MongoDB database '{self.db_name}'.")
        except ConnectionError as e:
            print(f"Could not connect to MongoDB: {e}")
            self.client = None
            self.db = None
            self.collection = None
    
    def get_database():
        client = MongoClient(MONGO_URI)
        return client[DATABASE_NAME]

    def store_search_data(self, url, category, summary):
        if self.collection is None:
            print("Database connection is not established. Cannot store data.")
            return

        search_data = {
            "url": url,
            "category": category,
            "summary": summary
        }
        try:
            inserted_result = self.collection.insert_one(search_data)
            
        except Exception as e:
            print(f"An error occurred while storing data for '{url}': {e}")

    def search_by_keyword(self, keyword: str) -> List[Dict]:
        
        query = {
            "$or": [
                {"url": {"$regex": keyword, "$options": "i"}},
                {"category": {"$regex": keyword, "$options": "i"}},
                {"summary": {"$regex": keyword, "$options": "i"}}
            ]
        }
        results = list(self.collection.find(query))
        return results
    
    def close_connection(self):
        if self.client:
            self.client.close()
            print("MongoDB connection closed.")
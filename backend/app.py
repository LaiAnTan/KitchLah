from flask import Flask, Response, request
from pymongo import MongoClient
from pymongo.collection import Collection
from dotenv import load_dotenv
import random
import json
import os 

load_dotenv()

app = Flask(__name__)
mongo_uri = os.getenv("MONGO_URI")

class MongoDB:
   _instance = None
   db = None

   def __new__(cls, *args, **kwargs):
      if not cls._instance:
         cls._instance = super(MongoDB, cls).__new__(cls, *args, **kwargs)
         cls.db = MongoClient(mongo_uri)[os.getenv("MONGO_DB")]
      return cls._instance

class MongoCollection:
    collection: Collection = None

    def __init_subclass__(cls, collection_name, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.collection = MongoDB().db[collection_name]

    @classmethod
    def patch(cls, id, data):
        update_operations = {"$set": data}
        return cls.collection.update_one({"_id": id}, update_operations)

    @classmethod
    def post(cls, data):
        return cls.collection.insert_one(data)

    @classmethod
    def get_all(cls):
        return list(cls.collection.find({}))

    @classmethod
    def get(cls, id):
        return cls.collection.find_one({"_id": id})

    @classmethod
    def delete(cls, id):
        return cls.collection.delete_one({"_id": id})

class TestOne(MongoCollection, collection_name="testone"):
   pass

class TestTwo(MongoCollection, collection_name="testtwo"):
    pass

@app.route('/post', methods=["GET"])
def post():
   TestOne.post({
      'number': random.randint(1, 10**9)
   })
   return 'Post Done :D'

@app.route('/get', methods=["GET"])
def get():
   data = TestOne.get_all()
   return json.dumps(data, default=str)

if __name__ == '__main__':
   app.run()
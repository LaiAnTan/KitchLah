from pymongo import MongoClient
from config import Config

class Database:
    _instance = None
    _client = None
    _db = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._client = MongoClient(Config.MONGODB_URI)
            cls._db = cls._client[Config.DATABASE_NAME]
        return cls._instance

    @property
    def client(self):
        return self._client

    @property
    def db(self):
        return self._db

    @property
    def ingredients(self):
        return self._db.ingredients

    @property
    def schedules(self):
        return self._db.schedules

    @property
    def restocks(self):
        return self._db.restocks

    def close(self):
        if self._client:
            self._client.close()

# Global database instance
db = Database()
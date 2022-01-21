import pymongo
import certifi
from pymongo import MongoClient
from typing import Dict

class Database:

    URI = "mongodb+srv://justin:Justin123@microblog.fcu71.mongodb.net/test"
    DATABASE = None

    @staticmethod
    def initialize():
        client = pymongo.MongoClient(Database.URI, tlsCAFile=certifi.where())
        Database.DATABASE = client["Pricing"]

    @staticmethod
    def insert(collection: str, data: Dict):
        Database.DATABASE[collection].insert_one(data)

    @staticmethod
    def find(collection: str, query: Dict) -> pymongo.cursor:
        return Database.DATABASE[collection].find(query)

    @staticmethod
    def find_one(collection: str, query: Dict) -> Dict:
        return Database.DATABASE[collection].find_one(query)

    #upsert = True updates the db id no unique id is found
    @staticmethod
    def update(collection: str, query: Dict, data: Dict) -> None:
        #had to use replace_one as update did not work
        Database.DATABASE[collection].replace_one(query, data, upsert=True)

    @staticmethod
    def remove(collection: str, query: Dict) -> Dict:
        return Database.DATABASE.remove(collection, query)



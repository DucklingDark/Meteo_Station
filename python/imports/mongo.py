from pymongo import MongoClient

class Mongo():
    def __init__(self, client, db, coll):
        self.client     = MongoClient(client)
        self.database   = self.client[db]
        self.collection = self.database[coll]
        self.db_str     = 'Database --> ' + db + '\t\tCollection --> ' + coll 


    def write(self, dict):
        x = self.collection.insert_one(dict)
        str = 'Inserted to MongoDB: ', x.inserted_id
        print(str)
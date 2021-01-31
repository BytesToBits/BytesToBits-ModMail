from pymongo import MongoClient
from .files import Data

import datetime

config = Data("config").yaml_read()

client = MongoClient(config["mongo-uri"])

class Snippets:
    def __init__(self):
        self.snippets = client["neki"]["snippets"]

    def get_all(self):
        return [snippet for snippet in self.snippets.find({})]
        
    def get(self, **kwargs):
        r = self.snippets.find_one(kwargs)
        return r
    
    def add_snippet(self, name, content):
        self.snippets.insert_one({
            "_id":name,
            "content":content
            })

    def delete_snippet(self, name):
        self.snippets.delete_one({
            "_id":name
        })

class Threads:
    def __init__(self, thread=None):
        self.thread = thread
        self.col = client["neki"]["threads"]

    def create_thread(self, **kwargs):
        kwargs["_id"] = self.thread
        self.col.insert_one(kwargs)
    
    def exists(self, **checks):
        r = self.col.find_one(checks)
        if r: return True
        return False

    def get_all(self):
        return [r for r in self.col.find({})]
    
    def get(self, **kwargs):
        r = self.col.find_one(kwargs)
        return r
    
    def data(self):
        r = self.col.find_one({"_id":self.thread})
        return r

    def update_thread(self, **kwargs):
        self.col.update_one({"_id":self.thread}, {"$set":kwargs})

    @property
    def delete(self):
        self.col.delete_one({"_id":self.thread})

class Logs:
    def __init__(self, thread:int):
        self.thread = thread
        self.db = client["neki_logs"]
    
    def add_message(self, message, mod=False, system=False):
        if not Threads(self.thread).exists: return
        col = self.db[f"logs_{self.thread}"]
        post = {
            "_id": message.id,
            "recipient": Threads().get(_id=self.thread)['recipient'],
            "content": message.content,
            "author": str(message.author),
            "author_avatar": str(message.author.avatar_url_as(static_format="png")),
            "date": datetime.datetime.utcnow(),
            "system": system,
            "mod": mod
        }
        col.insert_one(post)
    
    def edit_message(self, message):
        if not Threads(self.thread).exists: return
        col = self.db[f"logs_{self.thread}"]
        col.update_one({"_id":message.id}, {"$set":{"content":message.content}})
    
    def delete_message(self, message, _id=None):
        if not Threads(self.thread).exists: return
        col = self.db[f"logs_{self.thread}"]
        if not _id:
            col.delete_one({"_id":message.id})
        else:
            col.delete_one({"_id":_id})

    def get(self, **kwargs):
        if not Threads(self.thread).exists: return
        col = self.db[f"logs_{self.thread}"]
        r =  col.find_one(kwargs)
        return r

    def get_all(self):
        if not Threads(self.thread).exists: return
        col = self.db[f"logs_{self.thread}"]
        return [i for i in col.find({})]
    
    def store_logs(self, userID):
        cols = self.db.list_collection_names()
        print(cols)
        r = []
        for col in cols:
            if self.db[col].find({"recipient":int(userID)}):
                r.append(col)
        return r
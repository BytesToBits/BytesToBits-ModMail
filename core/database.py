from pymongo import MongoClient
from .files import Data

config = Data("config").yaml_read()

client = MongoClient(config["mongo-uri"])

class Threads:
    def __init__(self, thread=None):
        self.thread = thread
        self.col = client["pug"]["threads"]

    def create_thread(self, **kwargs):
        kwargs["_id"] = self.thread
        self.col.insert_one(kwargs)

    def exists(self, **checks):
        return self.col.find_one(checks)

    def get(self, **kwargs):
        return self.col.find_one(kwargs)

    @property
    def delete(self):
        self.col.delete_one({"_id":self.thread})

    def fetch_all(self):
        for coll in self.coll.list_collection_names():
            print(coll)

class Logs:
    def __init__(self, thread:int):
        self.thread = thread
        self.db = client["logs"]

    def add_message(self, message, mod=False):
        if not Threads(message.channel.id).exists: return
        col = self.db[f"logs_{self.thread}"]
        post = {
            "_id": message.id,
            "content": message.content,
            "author": str(message.author),
            "author_avatar": str(message.author.avatar_url_as(static_format="png")),
            "mod": mod
        }
        col.insert_one(post)

    def fetch(self):
        cursor = self.db[f"logs_{self.thread}"].find({})
        messages = [message for message in cursor]
        return messages

    def fetch_all(self):
        for coll in self.db.list_collection_names():
            print(coll)

        ## Never mind that I will continue it once I have a clear picture of how I want it to be.

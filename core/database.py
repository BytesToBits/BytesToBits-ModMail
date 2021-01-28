from pymongo import MongoClient
from .files import Data

config = Data("config").json_read

client = MongoClient(config["mongo-uri"])

class Threads:
    def __init__(self, thread=None):
        self.thread = thread
        self.col = client["main"]["threads"]

    def create_thread(self, **kwargs):
        kwargs["_id"] = self.thread
        self.col.insert_one(kwargs)
    
    def exists(self, **checks):
        return self.col.find_one(checks)
    
    def get(**kwargs):
        return self.col.find_one(kwargs)

    @property
    def delete(self):
        self.col.delete_one({"_id":self.thread})

class Logs:
    def __init__(self, thread:int):
        self.thread = thread
        self.db = client["logs"]
    
    def add_message(self, message, mod=False, system=False):
        if not Threads(message.channel.id).exists: return
        col = self.db[f"logs_{thread}"]
        post = {
            "_id": message.id,
            "content": message.content,
            "author": str(message.author),
            "author_avatar": message.author.avatar_url_as(static_format="png"),
            "system": system,
            "mod": mod
        }
        ## Never mind that I will continue it once I have a clear picture of how I want it to be.
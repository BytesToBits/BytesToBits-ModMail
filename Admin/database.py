import pymongo
from Admin.admin import Files

cluster = pymongo.MongoClient(Files.config("main", "mongo"))
db = cluster["main"]
threads = db["threads"]
snippets = db["snippets"]
blocks = db["blocks"]

class Blocks:
  def exists(name):
    r = blocks.find_one({"_id":name.id})
    if not r: return False
    return True
  
  def add(name, operator, reason):
    blocks.insert_one(
      {"_id":name.id,
      "operator":operator.id,
      "reason":reason}
    )
  
  def delete(name):
    blocks.delete_one(
      {
        "_id":name.id
      }
    )
  
  def update(name, data):
    blocks.update_one({"_id":name.id}, {"$set":data})

  def get(name):
    r = blocks.find_one({"_id":name.id})
    return r
  
  def get_all():
    r = blocks.find({})
    return [i for i in r]

class Snippets:
  def exists(name):
    r = snippets.find_one({"_id":name})
    if not r: return False
    return True
  
  def add(name, content):
    snippets.insert_one(
      {"_id":name,
      "content":content}
    )
  
  def delete(name):
    snippets.delete_one(
      {
        "_id":name
      }
    )
  
  def update(name, content):
    snippets.update_one({"_id":name}, {"$set":{"content":content}})

  def get(name):
    r = snippets.find_one({"_id":name})
    return r
  
  def get_all():
    r = snippets.find({})
    return [i for i in r]
    
class Threads:
  def exists(channel):
    r = threads.find_one({"_id":channel.id})
    if not r: return False
    return True
  
  def get_all():
    results = threads.find({})
    return [i for i in results]
  
  def get(channel):
    r = threads.find_one({"_id":channel.id})
    return r
  
  def find(data):
    r = threads.find_one(data)
    return r

  def add(channel, message):
    threads.insert_one({
      "_id":channel.id,
      "recipient":message.author.id,
      "channel":message.channel.id,
      "close":None,
      "notify":None,
      "subscribed":None,
      "messages": {}
    })

  def raw_add(data):
    threads.insert_one(data)

  def delete(channel):
    threads.delete_one({"_id":channel.id})
  
  def raw_delete(channel_id):
    threads.delete_one({"_id":channel_id})

  def update(channel, values):
    threads.update_one({"_id":channel.id}, {"$set":values})

  def add_message(channel, message, botmsg):
    messages = Threads.get(channel)["messages"]
    messages[str(botmsg.id)] = message.id
    Threads.update(channel, {"messages":messages})
  
  def delete_message(channel, botmsg):
    messages = Threads.get(channel)["messages"]
    try:
      del messages[str(botmsg.id)]
    except:
      pass
    Threads.update(channel, {"messages":messages})
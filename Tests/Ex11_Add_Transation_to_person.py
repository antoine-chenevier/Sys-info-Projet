import redis
import random
from datetime import datetime
import json
import hashlib

# Connect to redis database
redis_host = 'localhost'
redis_port = 6379
redis_db = 0
redis_client = redis.Redis(host=redis_host, port=redis_port, db=redis_db, decode_responses=True)

transaction_keys = redis_client.keys() # Get all keys in the DB

if transaction_keys:
    random_key = random.choice(transaction_keys) # Choose a random key from the transactions list
    random_value = redis_client.get(random_key) # Get the value of that key
    if random_value: # Check if the value is not None
        value = json.loads(random_value) # Load transation
        person = value[0]
else:
    print("Database doesn't have any keys")


# Define a transation
sender = person
sent_to = "christian"
transation_amount = str(5000)
current_time =  datetime(2023,1,1).timestamp()
hash = hashlib.sha256((sender + sent_to + transation_amount + str(current_time)).encode()).hexdigest()
transation = json.dumps([sender,sent_to,current_time,transation_amount,hash])
transaction_key = f"{sender}_{sent_to}"
redis_client.set(transaction_key,transation) 

# Check if the transaction was added
if redis_client.get(transaction_key):
    print("Transaction added successfully!")
else:
    print("Transaction not added!")

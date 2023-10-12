import redis
import json
from datetime import datetime
import random

# Connect to redis database
redis_host = 'localhost'
redis_port = 6379
redis_db = 0
redis_client = redis.Redis(host=redis_host, port=redis_port, db=redis_db, decode_responses=True)
 
transaction_keys = redis_client.keys() # Get all the keys in the database

# Loop through the keys and modify all of them
for key in transaction_keys:
    existing_transaction_val = redis_client.get(key) # Get each transation in the DB
    if existing_transaction_val:
        existing_transaction = json.loads(existing_transaction_val)
        new_transaction_amout = random.randrange(0,9999) # Change the current transtaion amount to a random value
        existing_transaction[3] = new_transaction_amout # Modify the transation amount
        modified_transaction_val = json.dumps(existing_transaction)
        redis_client.set(key, modified_transaction_val) # Set the new transation amount

print("Transation modified successfully. ")

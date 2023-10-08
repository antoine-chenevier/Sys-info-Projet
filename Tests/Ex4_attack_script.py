import redis
import json
from datetime import datetime
import random

# Connect to redis database
redis_host = 'localhost'
redis_port = 6379
redis_db = 0
redis_client = redis.Redis(host=redis_host, port=redis_port, db=redis_db, decode_responses=True)
 
transation_keys = redis_client.keys() # Get all the keys in the database

# Loop through the keys and modify all of them
for key in transation_keys:
    existing_transation_val = redis_client.get(key) # Get each transation in the DB
    if existing_transation_val:
        existing_transation = json.loads(existing_transation_val)
        new_transation_amout = random.randrange(0,9999) # Change the current transtaion amount to a random value
        existing_transation[3] = new_transation_amout # Modify the transation amount
        modified_transation_val = json.dumps(existing_transation)
        redis_client.set(key, modified_transation_val) # Set the new transation amount

print("Transation modified successfully. ")

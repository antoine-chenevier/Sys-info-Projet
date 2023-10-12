import redis
import random

# Connect to redis database
redis_host = 'localhost'
redis_port = 6379
redis_db = 0
redis_client = redis.Redis(host=redis_host, port=redis_port, db=redis_db, decode_responses=True)

transaction_keys = redis_client.keys() # Get all keys in the DB

if transaction_keys:
    random_key = random.choice(transaction_keys) # Choose a random key from the transactions list
    random_value = redis_client.get(random_key) # Get the value of that key
    redis_client.delete(random_key) # Delete transaction
    print(f"Successfully deleted transation: {random_value} from the DB")
else:
    print("Database doesn't have any keys to delete!")

from flask import Flask, request
from datetime import datetime, timedelta
import time
import redis
import json
import hashlib

app = Flask(__name__)

r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
r1 = redis.Redis(host='localhost', port=6379, db=1,decode_responses=True)

# Get the current date in second since 01-01-2023, add seconds and milliseconds
current_time = time.time()
transations = [] 


# Function to return all of the dictionary
@app.route("/display_list", methods=['GET'])
def getList():
    if request.method == 'GET':

        # Load transations from the database ONLY THE FIRST TIME
        if len(transations) == 0:
             for key in r.keys():
                if key:
                    transation = json.loads(r.get(key))
                    transations.append(transation)
       
        # Sort the dictionary by date
        return str(transations)


# Function to add an element in the dictionary
@app.route("/add_element/", methods=['POST','GET'])
def addElement():
    if request.method == 'POST':

        # Get the data from the form
        person1=str(request.form.get("p1"))    
        person2=str(request.form.get("p2"))
        solde=int(request.form.get("solde"))

        # Get the current date in second since 2023
        time = datetime(2023,1,1).timestamp()

        # Initialize the tupple
        add = (person1,person2,time,solde,None)

        # Compute the hash and update the tuple
        previous_hash = None if len(transations) == 0 else transations[-1][-1] # Get the previous hash (skip if its the first element in the transations list)
        add = (*add[:-1], compute_hash(add,previous_hash))  # Compute the hash after adding the previous_hash

        # Add the element in a tuple
        add_str = json.dumps(add)
        key = "add" + str((len(transations) + 1))
        r.set(key,add_str)
    
        # Add the tuple in the dictionary!
        transations.append(add)


        return "You have successfully added a new element:" + str(add)
    return "You have not added a new element"
# Endpoint to check if all the transations hash is correct
@app.route("/check_integrity", methods=['GET'])
def checkIntegrity():
    previous_hash = None
    for i, transaction_tuple in enumerate(transations):
        recalculated_hash = compute_hash(transaction_tuple, previous_hash)
        stored_hash = transaction_tuple[-1]  # Extract the stored hash from the tuple
        if recalculated_hash != stored_hash: # Check if the calculated hash is equal to the stored hash
            return f"Integrity check failed for transaction {i+1}" # A transaction has been modified
        previous_hash = recalculated_hash  # Update previous_hash for the next iteration
    return "Integrity check passed for all transactions" # All transactions have not been modified

# Method to compute the hash
def compute_hash(transaction_tuple, previous_hash=None):
    transaction = list(transaction_tuple[:-1])  # Remove the last element from the transaction tuple which contains the hash 
    data_str = json.dumps(transaction + [previous_hash], sort_keys=True)  # Convert to JSON object
    return hashlib.sha256(data_str.encode()).hexdigest()  # Use SHA-256 function
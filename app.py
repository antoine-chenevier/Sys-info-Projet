from flask import Flask, request
from datetime import datetime, timedelta
import time
import redis
import json
import hashlib

app = Flask(__name__)

r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

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
       
        # Return the list
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
        
        # Get the previous hash (skip if its the first element in the transations list)
        previous_hash = None if len(transations) == 0 else transations[-1][-1] 

        # Compute the hash after adding the previous_hash
        add = (*add[:-1], compute_hash(add,previous_hash))  

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
        
        # Extract the stored hash from the tuple
        stored_hash = transaction_tuple[-1]  
        
        # Check if the calculated hash is equal to the stored hash
        if recalculated_hash != stored_hash: 

            # A transaction has been modified
            return f"Integrity check failed for transaction {i+1}" 
        
        # Update previous_hash for the next iteration
        previous_hash = recalculated_hash  

        # All transactions have not been modified
    return "Integrity check passed for all transactions" 

# Method to compute the hash 
def compute_hash(transaction_tuple, previous_hash=None):

    # Remove the last element from the transaction tuple which contains the hash 
    transaction = list(transaction_tuple[:-1])  

    # Convert to JSON object and sort the keys
    data_str = json.dumps(transaction + [previous_hash], sort_keys=True)  

    # Use SHA-256 function to compute the hash
    return hashlib.sha256(data_str.encode()).hexdigest()  
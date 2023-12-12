from flask import Flask, request
from datetime import datetime, timedelta
import time
import redis
import json
import hashlib
import rsa
from flask import jsonify

app = Flask(__name__)

r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

# Get the current date in second since 01-01-2023, add seconds and milliseconds
current_time = time.time()

# Initialize the dictionary
transactions = [] 


# Function to return all of the dictionary
@app.route("/display_list", methods=['GET'])
def getList():
    if request.method == 'GET':

        # Load transactions from the database ONLY THE FIRST TIME
        if len(transactions) == 0:
             for key in r.keys():
                if key:
                    transation = json.loads(r.get(key))
                    transactions.append(transation)
       
        # Return the list
        return str(transactions)


# Générer une paire de clés (publique et privée)
(pubkey, privkey) = rsa.newkeys(512)

# Fonction pour ajouter un élément à la liste
@app.route("/add_element", methods=['POST'])
def addElement():
    if request.method == 'POST':
     
        # Get the data from the form
        person1=str(request.form.get("p1"))    
        person2=str(request.form.get("p2"))
        solde=int(request.form.get("solde"))

        # Get the current date in second since 2023
        time = datetime(2023,1,1).timestamp()

        # Initialize the dictionary
        add = {
            'person1': person1,
            'person2': person2,
            'time': time,
            'solde': solde,
            'signature': None
        }

        # Signer la transaction avec la clé privée de l'expéditeur
        signature = rsa.sign(json.dumps(add).encode(), privkey, 'SHA-256')

        # Ajouter la signature à la transaction
        add['signature'] = signature.hex()

        # Ajouter la transaction à la liste des transactions
        transactions.append(add)

        # Stocker la transaction dans la base de données Redis
        r.set(hashlib.sha256(json.dumps(add).encode()).hexdigest(), json.dumps(add))

        # Retourner une réponse
        return jsonify({'message': 'Transaction ajoutée avec succès !'}), 200
    return "You have not added a new element"

# Endpoint to check if all the transactions hash is correct
@app.route("/check_integrity", methods=['GET'])
def checkIntegrity():

    previous_hash = None
    for i, transaction_tuple in enumerate(transactions):

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
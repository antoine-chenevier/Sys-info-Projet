from flask import Flask, request
from datetime import datetime
import time
import redis
import json
import hashlib
from flask import jsonify
import rsa


app = Flask(__name__)

r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

# Get the current date in second since 01-01-2023, add seconds and milliseconds
current_time = time.time()

# Initialize the dictionary
transactions = [] 

# Générer une paire de clés (publique et privée)
(pubkey, privkey) = rsa.newkeys(512)



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


# Fonction pour ajouter un élément à la liste
@app.route("/add_element/", methods=['POST','GET'])
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
            'solde': solde
        }

        # Sign the transaction with the sender's private key
        # signature = r.set(hashlib.sha256(json.dumps(add).encode()).hexdigest(), json.dumps(add))

        message = json.dumps(add, sort_keys=True).encode() # Convert the transation to a JSON string
        hash = hashlib.sha256(message).digest()# Create a hash of the message
        signature = rsa.sign(hash,privkey,'SHA-256') # Sign the hash with the private key
        signature_hex = signature.hex() # Convert the signature to hex
        add['signature'] = signature_hex # Add the signature to the transaction
        add['hash'] = hash.hex() # Add the hash to the transaction
        transactions.append(add) # Ajouter la transaction à la liste des transactions


        # Stocker la transaction dans la base de données Redis
        r.set(hashlib.sha256(json.dumps(add).encode()).hexdigest(), json.dumps(add))

        # Retourner une réponse
        return jsonify({'message': 'Transaction ajoutée avec succes !'}), 200
    return "You have not added a new element"

# Endpoint to check if all the transactions hash is correct
@app.route("/check_integrity/", methods=['GET'])
def checkIntegrity():

    for i in range(len(transactions)):
        
        # Get the current transaction
        current_transaction = transactions[i]

        # Get the parts of the transaction that were signed
        signed_data = {key: current_transaction[key] for key in current_transaction if key != 'signature'}
        try:
            # Verify the signature
            rsa.verify(bytes.fromhex(current_transaction['hash']),bytes.fromhex(current_transaction['signature']),pubkey)
        except rsa.pkcs1.VerificationError:
            print("Verification failed")
            return jsonify({"error": "Integrity check failed"}), 400

    return "Toutes les transactions rsa sont correctes"
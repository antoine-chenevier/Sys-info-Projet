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


@app.route("/display_list", methods=['GET'])
def getList():
    if request.method == 'GET':

        if len(transactions) == 0:
             for key in r.keys():
                if key:
                    transation = json.loads(r.get(key))
                    transactions.append(transation)
       
        return str(transactions)


(pubkey, privkey) = rsa.newkeys(512)

@app.route("/add_element/", methods=['POST','GET'])
def addElement():

    if request.method == 'POST':
     
        person1=str(request.form.get("p1"))    
        person2=str(request.form.get("p2"))
        solde=int(request.form.get("solde"))

        time = datetime(2023,1,1).timestamp()

        add = {
            'person1': person1,
            'person2': person2,
            'time': time,
            'solde': solde,
            'signature': None
        }

        signature = rsa.sign(json.dumps(add).encode(), privkey, 'SHA-256')

        add['signature'] = signature.hex()

        transactions.append(add)

        r.set(hashlib.sha256(json.dumps(add).encode()).hexdigest(), json.dumps(add))

        return jsonify({'message': 'Transaction ajoutée avec succes !'}), 200
    return "You have not added a new element"

@app.route("/check_integrity/", methods=['GET'])
def checkIntegrity():

    for i in range(len(transactions)):
        
        current_transaction = transactions[i]

        if isinstance(current_transaction, dict) and 'signature' in current_transaction:
            try:
                rsa.verify(json.dumps(current_transaction).encode(), bytes.fromhex(current_transaction['signature']), pubkey)
            except rsa.VerificationError:
                return "La signature de la transaction " + str(i) + " est incorrecte"
        else:
            return "La transaction " + str(i) + " n'est pas un dictionnaire avec une clé 'signature'"

    return "Toutes les transactions rsa sont correctes"
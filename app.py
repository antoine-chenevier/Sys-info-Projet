from flask import Flask, request
from datetime import datetime
import redis
import json
import hashlib

app = Flask(__name__)

r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
r1 = redis.Redis(host='localhost', port=6379, db=1,decode_responses=True)

# Get the current date in second since 01-01-2023
time = datetime(2023,1,1).timestamp() 

# Tuple initialization
# Structure of a transation (P1,P2,t,a,h)
add1 = ("Antoine","Christian",time,10,None)
add2 = ("Antoine","Christian",time,200,None)

# Convert the tuples to JSON strings
add1_json = json.dumps(add1)
add2_json = json.dumps(add2)

# Store the JSON strings in Redis
r.set("add1", add1_json)
r.set("add2", add2_json)

# Dictionary initialization
transations = [add1,add2]


# Function to return all of the dictionary
@app.route("/display_list", methods=['GET'])
def getList():
    if request.method == 'GET':

        # Sort the dictionary by date
        transations.sort()
        return str(transations)


# Function to return all of the dictionary of a person
@app.route("/display_list/<Person>", methods=['GET'])
def getListPerson(Person):
    if request.method == 'GET':

        # Initialize the result
        result = ""

        # Sort the dictionary by date
        transations.sort()

        # Loop through the dictionary
        for i in transations:

            # Check if the person in the dictonary is egal to the person in the GET
            if i[0] == Person:
                result+= str(i)
            if i[1] == str(Person):
                result+= str(i)

        # If the person is not in the dictionary
        if(result == ""):
            return "Person not found"

        # If the person is in the dictionary return the solde of transations
        else:
            return result


# Function to display  the solde of a person
@app.route("/display_solde/<Person>", methods=['GET'])
def getSolde(Person):

    # Initialize the solde
    solde = 0

    # Loop through the dictionary
    for i in transations:

        # Check if the person in the dictonary is egal to the person in the GET
        if i[0] == Person:

            # Remove the solde of the person
            solde -= i[3]
        if i[1] == Person:

            # Add the solde of the person
            solde += i[3]
    return str(solde)


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
        add = (*add[:-1],compute_hash(add))

        # Add the element in a tuple
        add_str = json.dumps(add)
        key = "add" + str((len(transations) + 1))
        r.set(key,add_str)
    
        # Add the tuple in the dictionary
        transations.append(add)


        return "You have successfully added a new element:" + str(add)
    return "You have not added a new element"

# Endpoint to check if all the transations hash is correct
@app.route("/check_integrity", methods=['GET'])
def checkIntegrity():
    for i,transaction_tuple in enumerate(transations):
        recalculated_hash = compute_hash(transaction_tuple[:-1])
        if recalculated_hash != transaction_tuple[:-1]:
            return f"Integrity check failed for transation {i+1}"
    return "Integrity check passed for all transations"
# THIS IS STILL NOT WORKING !!!!


# Method to compute the hash
def compute_hash(transation_tuple):
    transation = transation_tuple[:-1] # Remove the last element from the transtation tuple which contains the hash 
    data_str = json.dumps(transation, sort_keys = True) # Convert to JSON object
    return hashlib.sha256(data_str.encode()).hexdigest() # Use SHA-256 function


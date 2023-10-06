from flask import Flask, request
from datetime import datetime
import redis
import json

app = Flask(__name__)

r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
r1 = redis.Redis(host='localhost', port=6379, db=1,decode_responses=True)

# Get the current date in second since 01-01-2023
time = datetime(2023,1,1).timestamp() 

# Tuple initialization
add1 = ("Antoine","Christian",time,10)
add2 = ("Antoine","Christian",time,200)

# Convert the tuples to JSON strings
add1_json = json.dumps(add1)
add2_json = json.dumps(add2)

# Store the JSON strings in Redis
r.set("add1", add1_json)
r.set("add2", add2_json)

# Dictionary initialization
transaction = [add1,add2]


# Function to return all of the dictionary
@app.route("/display_list", methods=['GET'])
def getList():
    if request.method == 'GET':

        # Sort the dictionary by date
        transaction.sort()
        return str(transaction)


# Function to return all of the dictionary of a person
@app.route("/display_list/<Person>", methods=['GET'])
def getListPerson(Person):
    if request.method == 'GET':

        # Initialize the result
        result = ""

        # Sort the dictionary by date
        transaction.sort()

        # Loop through the dictionary
        for i in transaction:

            # Check if the person in the dictonary is egal to the person in the GET
            if i[0] == Person:
                result+= str(i)
            if i[1] == str(Person):
                result+= str(i)

        # If the person is not in the dictionary
        if(result == ""):
            return "Person not found"

        # If the person is in the dictionary return the solde of transaction
        else:
            return result


# Function to display  the solde of a person
@app.route("/display_solde/<Person>", methods=['GET'])
def getSolde(Person):

    # Initialize the solde
    solde = 0

    # Loop through the dictionary
    for i in transaction:

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

        # Add the element in a tuple
        add = (person1,person2,time,solde)
        r.save(add)
    
        # Add the tuple in the dictionary
        transaction.append(add)

    

        return "You have successfully added a new element:" + str(add)
    return "You have not added a new element"

---
runme:
  id: 01HHDEBE0MGX2DD7V6Y9J3DZB4
  version: v2.0
---

# Sys-info-Projet

# Auteur

antoine chenevier
email antoine.chenevier01@gmail.com

christian Hasbani
email christian_hasbani@etu.u-bourgogne.fr

# My Flask Application

This is a simple Flask application.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

You need to have Python and all the requirements installed on your machine. 

```bash
pip install -r requirements.txt
```
## Clone the project

git clone https://github.com/antoine-chenevier/

## Run the application 

## curl

Here are examples of `curl` commands to access the different routes in [app.py](./app.py)

### Route `/display_list`

```python {"id":"01HHDEBE0K6CRD61G4879Q8C5P"}
@app.route("/display_list", methods=['GET'])
def getList():
    ...
```

```bash {"id":"01HHDEBE0K6CRD61G488VK8FBE"}
curl -X GET http://localhost:5000/display_list

```

Function to return all of the dictionary

### Route `/display_list/<Person>`

```python {"id":"01HHDEBE0K6CRD61G48ABJKSQK"}
@app.route("/display_list/<Person>", methods=['GET'])
def getListPerson(Person):
  ...

```

```bash {"id":"01HHDEBE0K6CRD61G48CVNNRGT"}
curl -X POST -d "Person=person" http://localhost:5000/display_list/<Person>

```

Function to return all of the dictionary of a person

### Route `/display_solde/<Person>`

```python {"id":"01HHDEBE0K6CRD61G48E4C3DGZ"}
@app.route("/display_solde/<Person>", methods=['GET'])
def getSolde(Person):
  ...

```

```bash {"id":"01HHDEBE0K6CRD61G48GX9RQM3"}
curl -X GET -d "Person=person" http://localhost:5000/display_solde/<Person>

```

Function to display  the solde of a person

### Route `/add_element/`

```python {"id":"01HHDEBE0K6CRD61G48JMG8ZGV"}
@app.route("/add_element/", methods=['POST','GET'])
def addElement():
  ...
```

```bash {"id":"01HHDEBE0K6CRD61G48PDSQYBX"}
curl -X GET http://loccurl -X POST http://localhost:5000/add_element/ -d "p1=christian&p2=antoine&solde=10"

```

Function to add an element in the dictionary

### Route `check_integrity`

```python {"id":"01HHDEBE0MGX2DD7V6XJGA3CKS"}
@app.route("/check_integrity", methods=['GET'])
def checkIntegrity():
    ...
```

```bash {"id":"01HHDEBE0MGX2DD7V6XJNE3K6T"}
curl -X GET http://localhost:5000/check_integrity

```

Function to recalculate all the hashes of the transaction checking if there has been any modifications

## Attacking the system in V1

### Objective

Modify the amout of a transaction directly in the data file

#### 1- Identify the data file

According to our code the transactions are being stored in the a redis database which is an open-source, in-memory data structure NoSQL Database that using key-value method of storing data.

Here it is used to store each transaction using a key.

#### 2- Manually edit the amout of a transaction in the file

Here we will use a python scripts saved in the tests folder to connect to the redis database and manually modify the saved transaction keys

### Testing the script

We start by running the python file in tests directory

Then we connect to the redis DB

```bash {"id":"01HHDEBE0MGX2DD7V6XP2TGG2J"}
redis-cli

```

Then we check the value of address 1 for example

```bash {"id":"01HHDEBE0MGX2DD7V6XR1JH7J4"}
127.0.0.1:6379> GET add1
"[\"Antoine\", \"Christian\", 1672527600.0, 5]"

```

```bash {"id":"01HHDEBE0MGX2DD7V6XRMA5WNC"}
python3 Ex4_attack_script.py

```

Then we check the new keys values

```bash {"id":"01HHDEBE0MGX2DD7V6XSHYM4G4"}
GET add1

```

We will see this output

```bash {"id":"01HHDEBE0MGX2DD7V6XV4XB2TS"}
127.0.0.1:6379> GET add1
"[\"Antoine\", \"Christian\", 1672527600.0, 9034]"

```

So as we can see the transaction amout has been modified

## Hash function in V2

Here we chose the SHA-256 for hashing the transactions, and we chose this functions for multiple reasons:

1- Security strength: SHA-256 is part of the SHA-2 family, which has shown to provide a higher level of security compared to its previous hashing algorithms

2- Collision resistance: the SHA-256 is designed to be collision-resistant meaning it's highly unlikely for two different inputs to produce the same hash value.

3- Widely used: SHA-256 is widely used and supported in various programming languages and cyptographic libraries, which allows for easy impelentation.

4- Standardization: SHA-256 is standarized by NIST (National Institute of Standards and Technology), making it a widely accepted and recommendded choice for cryptographic applications.

5- Performance: Even though the SHA-256 is more complicated than some simpler hash functions, it still performs well in practice.

6- Bit length: SHA-256 produces a 256-bit hash value, providing a large hash space that is more resistant to brute-force attacks.

## Verifying that that the attack script doesn't work anymore on our system

In exercise 4 we wrote a script to directly modify the data in the database.

Let's test this script again after implementing the hash function into our application.

Preview of the data before modifying it:

```bash {"id":"01HHDEBE0MGX2DD7V6XXGPRAHT"}
curl -X GET http://localhost:5000/display_list
[('benjamin', 'enzo', 1672527600.0, 30, 'c5abeb869ac53b8f132ecaf92ae99da4d7e2474ee529746bbf0fa75ff81d1323'), 
('calvin', 'enzo', 1672527600.0, 25, '71d3af238db66137346c9e8b884c320f0cc8ee2c14220aa0714052c1e8ed410e'), ('christian', 'antoine', 1672527600.0, 10, '7cc4f51e86fc29ed851d708f0f9f826dd7248cbf6e005d9e22401f8be163a829'), ('christian', 'enzo', 1672527600.0, 30, '8b311f3096ef6ff401dcae79b66dbd23edfa6324b4a07329b21680e7dce8e64b')]

```

And the data is the same in the DB

Then we run the check integrity to verify that it is working:

```bash {"id":"01HHDEBE0MGX2DD7V6XZZKASQE"}
curl -X GET http://localhost:5000/check_integrity
Integrity check passed for all transactions

```

Then we run the python scripts in tests

```bash {"id":"01HHDEBE0MGX2DD7V6Y062P9ZF"}
python3 Ex4_attack_script.py
transaction modified successfully.

```

we check the check intregrity endpoint again.

```bash {"id":"01HHDEBE0MGX2DD7V6Y08XAAMG"}
curl -X GET http://localhost:5000/check_integrity

```

And we will get a message

```bash {"id":"01HHDEBE0MGX2DD7V6Y2CKMKA3"}
Integrity check failed for transaction 1

```

Indicating that the transactions in our application have been modfied

## Attack script that deletes a transaction

In test folder we are going to use "Ex8_Delete_transactions.py"

```bash {"id":"01HHDEBE0MGX2DD7V6Y4P1HYQQ"}
python3 Ex8_Delete_transations.py
Successfully deleted transation: ["christian", "enzo", 1672527600.0, 5221, "8b311f3096ef6ff401dcae79b66dbd23edfa6324b4a07329b21680e7dce8e64b"] from the DB

```

After running this script we check again the display list endpoint and we will not find the transaction listed above
![image](https://github.com/antoine-chenevier/Sys-info-Projet/assets/117630923/cd50feb5-974c-4609-8ca4-5819da1d173d)

## Verifing the previous attack doesn't work

After changing the way we create the hash functions in our transations systems we will run the attack from the exercise 8 to test if the attack still works

First we verify that the check_integrity works on the current list we have

Here is the list of transations we have:

```bash {"id":"01HHDEBE0MGX2DD7V6Y4SFN8FS"}
christian@LAPTOP-179R2RO7:/mnt/d/VSCode/Sys-info-Projet$ curl -X GET http://localhost:5000/display_list
[('justin', 'antoine', 1672527600.0, 1000, 'a77898c497a60f295ca77558f90aea77bd1289c0b900fe49e9cace58638fdc97'), ('justin', 'christian', 1672527600.0, 150, '6da5fc48eb428479ad9d64693ae4328bfe9844612f366468860073a0ec419896'), ('calvin', 'christian', 1672527600.0, 30, 'e18846e06e5ad29128faada91d2d6cf7756f9d0732f7d2316da67d9c83516dd6')]

```

Then we verify the integrity of this list of transations:

```bash {"id":"01HHDEBE0MGX2DD7V6Y50ZNT06"}
christian@LAPTOP-179R2RO7:/mnt/d/VSCode/Sys-info-Projet$ curl -X GET http://localhost:5000/check_integrity
Integrity check passed for all transactions

```

### Launching the attack

Then we launch the attack script in the tests folder:

```bash {"id":"01HHDEBE0MGX2DD7V6Y6CEKFD2"}
christian@LAPTOP-179R2RO7:/mnt/d/VSCode/Sys-info-Projet/tests$ python3 Ex8_Delete_transactions.py 
Successfully deleted transation: ["calvin", "christian", 1672527600.0, 30, "e18846e06e5ad29128faada91d2d6cf7756f9d0732f7d2316da67d9c83516dd6"] from the DB

```

As observed we have deleted a transation from the transations list so let's verify if the check_integrity endpoint will detect error in this transations list:

```bash {"id":"01HHDEBE0MGX2DD7V6Y6WMKMXW"}
christian@LAPTOP-179R2RO7:/mnt/d/VSCode/Sys-info-Projet/tests$ curl -X GET http://localhost:5000/check_integrity
Integrity check failed for transaction 1

```

as we can see the check integrity failed since it calculated the hash for each element in the transations list and compared the values between the stored and the current values and detected a difference between the two.

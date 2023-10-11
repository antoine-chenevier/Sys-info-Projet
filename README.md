# Sys-info-Projet

# Auteur

antoine chenevier
email antoine.chenevier01@gmail.com

christian Hasbani
christian_hasbani@etu.u-bourgogne.fr

## curl

Here are examples of `curl` commands to access the different routes in [app.py](./app.py)

### route `/display_list`

```python
@app.route("/display_list", methods=['GET'])
def getList():
```

```bash
curl -X GET http://localhost:5000/display_list
```

Function to return all of the dictionary

### route `/display_list/<Person>`

```python
@app.route("/display_list/<Person>", methods=['GET'])
def getListPerson(Person):
  ...
```

```bash
curl -X POST -d "Person=person" http://localhost:5000/display_list/<Person>
```

Function to return all of the dictionary of a person

### route `/display_solde/<Person>`

```python
@app.route("/display_solde/<Person>", methods=['GET'])
def getSolde(Person):
  ...
```

```bash
curl -X GET -d "Person=person" http://localhost:5000/display_solde/<Person>
```

Function to display  the solde of a person

### route `/add_element/`

```python
@app.route("/add_element/", methods=['POST','GET'])
def addElement():
```

```bash
curl -X GET http://loccurl -X POST http://localhost:5000/add_element/ -d "p1=christian&p2=antoine&solde=10"
```

Function to add an element in the dictionary

### route `/importeCSV`

```python
@app.route("/importeCSV", methods=['GET'])
def importeCSV():
  ...
```

```bash
curl -d  "filePath=tab.csv" -X  GET http://localhost:5000/importeCSV

```

Function to import a CSV file

### route `/hash_verification`

```python
@app.route("/hash_verification", methods=['GET'])
def hash_vefication():
  ...
```

```bash
curl -X GET http://localhost:5000/hash_verification
```

Hash verification

### route `/hash_correction`

```python
@app.route("/hash_correctionn", methods=['GET'])
def hash_vefication():
  ...
```

```bash
curl -X GET http://localhost:5000/hash_correction
```

Hash correction

## Attacking the system in V1

### Objective 
Modify the amout of a transation directly in the data file

#### 1- Identify the data file

According to our code the transations are being stored in the a redis database which is an open-source, in-memory data structure NoSQL Database that using key-value method of storing data.

Here it is used to store each transation using a key.

#### 2- Manually edit the amout of a transation in the file

Here we will use a python scripts saved in the tests folder to connect to the redis database and manually modify the saved transation keys

### Testing the script

We start by running the python file in tests directory

Then we connect to the redis DB

```bash
redis-cli
```


Then We check the value of address 1 for example

```bash
127.0.0.1:6379> GET add1
"[\"Antoine\", \"Christian\", 1672527600.0, 5]"
```

```bash
python3 Ex4_attack_script.py
```

Then we check the new keys values 

```bash
GET add1
```
We will see this output

```bash
127.0.0.1:6379> GET add1
"[\"Antoine\", \"Christian\", 1672527600.0, 9034]"
```
So as we can see the transation amout has been modified

## Hash function in V2

Here we chose the SHA-256 for hashing the transations, and we chose this functions for multiple reasons:

  1- Security strength: SHA-256 is part of the SHA-2 family, which has shown to provide a higher level of security compared to its previous hashing algorithms

  2- Collision resistance: the SHA-256 is designed to be collision-resistant meaning it's highly unlikely for two different inputs to produce the same hash value. 

  3- Widely used: SHA-256 is widely used and supported in various programming languages and cyptographic libraries, which allows for easy impelentation.

  4- Standardization: SHA-256 is standarized by NIST (National Institute of Standards and Technology), making it a widely accepted and recommendded choice for cryptographic applications.

  5- Performance: Even though the SHA-256 is more complicated than some simpler hash functions, it still performs well in practice.

  6- Bit length: SHA-256 produces a 256-bit hash value, providing a large hash space that is more resistant to brute-force attacks.
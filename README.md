# Blockchain in Python from scratch

Understanding Blockchain isn't easy. At least it wasn't for me. I had to go through number of frustrations due to too few funcional examples of how this technology works. And I like learning by doing so if you do the same, allow me to guide you and by the end you will have a functioning Blockchain with a solid idea of how they work.

### Before you get started..

Remember that a Blockchain is an immutable, sequential chain of records called Blocks. They can contain transactions, files or any data you like, really. But the important thing is that they’re chained together using hashes.

### What is needed?

Make sure that you have Python 3.6+ installed (along with pip) and you will also need Flask and Requests library.

```sh
$ pip3 install -r requirements
```

You will also need an HTTP client like Postman or curl. But anything will do.

# Step 1: Building a Blockchain

So what does a block look like?

Each block has an index, timestamp, transactions, proof (more on that later) and a hash of the previous transaction.

Here is an example of what a single Block looks like:

```python
block = {
    'index': 1,
    'timestamp': 1506092455,
    'transactions': [
        {
            'sender': "852714982as982341a4b27ee00",
            'recipient': "a77f5cdfa2934hv25c7c7da5df1f",
            'amount': 5,
        }
    ],
    'proof': 323454734020,
    'previous_hash': "2cf24dba5fb0a3202h2025c25e7304249898"
}
```

### Represenging a Blockchain

We'll create a Blockchain class whose constructor creates a list to store our Blockchain and another to store transactions.  Here is how the Class will look like:

```python
class BlockChain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []

    @staticmethod
    def hash(block):
        pass

    def new_block(self):
        pass

    @property
    def last_block(self):
        return self.chain[-1]
```
This Blockchain class is responsible for managing the chain. It will store transactions and have helper functions.

The new_block method will create a new block and adds it on the chain and returns the last block in the chain.

The last_block method will return the last block in the chain.

Each block contains the hash and the hash of the previous block. This is what gives blockchains it's immutability - i.e. if anyone attack this, all subsequent blocks will be corrupt.

It's the core idea of blockchains. :)


### Adding transactions to the block

We will need some way of adding transactions to the block.

```python
class BlockChain(object):
    ...
    def new_transaction(self, sender, recipient, amount):
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })
        return self.last_block['index'] + 1
```

The new_transaction returns index of the block which will be added to current_transactions and is next one to be mined..

### Creating new blocks

In addition to creating the genesis block in our constructor, we will also need to flesh out methods for the new_block(), add_new_transaction() and hash().


```python
import hashlib
import json
import time

class BlockChain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        # create the genesis block
        self.new_block(previous_hash=1, proof=100)

    @staticmethod
    def hash(block):
        # hashes a block
        # also make sure that the transactions are ordered otherwise we will have insonsistent hashes!
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def new_block(self, proof, previous_hash=None):
        # creates a new block in the Blockchain
        block = {
            'index': len(self.chain)+1,
            'timestamp': time.time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }
        # reset the current list of transactions
        self.current_transactions = []
        self.chain.append(block)
        return block

    @property
    def last_block(self):
        # returns last block in the chain
        return self.chain[-1]

    def new_transaction(self, sender, recipient, amount):
        # adds a new transaction into the list of transactions
        # these transactions go into the next mined block
        self.current_transactions.append({
            "sender":sender,
            "recipient":recipient,
            "data":amount,
        })
        return int(self.last_block['index'])+1
```

Once our block is initiated, we need to feed it with the genesis block (a block with no predecessors). We will also need to add "a proof of work" to our genesis block which is the result of mining.

At this point, we're nearly done representing our Blockchain.

So lets talk about how the new blocks are created, forged and mined. :)


### Understanding Proof of Work

A proof of work algorithm are how new Blocks are created or mined on the Blockchain.

The goal is to discover a number that solves a problem.

The number must be difficult and resources consuming to find but super quick and easy to verify.

This is the core idea of Proof of Work.  :)


So lets work out some stupid-shit math problem that we are going to require to be solved in order for a block to be mined.

Lets say that hash of some integer ```x``` multiplied by another ```y``` must always end in 0.  So, as an example, the ```hash(x * y) = 4b4f4b4f54...0```.

```python
from hashlib import sha256

x = 5
y = 0 # we do not know what y should be yet
while sha256(f'{x*y}'.encode()).hexdigest()[-1] != "0": y+1

print(f'The solution is y = {y})
```

In this example we fixed the ```x = 5```.
The solution in this case is ```x = 5 ands y = 21``` since it procuced hash ```0```.

```python
hash(5 * 21) = "1253e9373e781b7500266caa55150e08e210bc8cd8cc70d89985e3600155e860"
```

In the Bitcoin world, the Proof of Work algorithm is called Hashcash. And it's not any different from the example above.  It's the very algorithm that miners race to solve in order to create a new block.  The difficulty is of course determined by the number of the characters searched for in the string. In our example we simplified it by defining that the resultant hash must end in 0 to make the whole thing in our case quicker and less resource intensive but this is how it works really.

The miners are rewarded for finding a solution by receiving a coin. In a transaction. There are many opinions on effectiness of this but this is how it works. And it really is that simple and this way the network is able to easily verify their solution. :)


### Implementing Proof of Work

Let's implement a similar algorithm for our Blockchain. Our rule will be similar to the example above.

"Find a number p that when hashed with the previous block's solution a hash with 4 leading 0 is produced."

```python
import hashlib
import json

from time import time
from uuid import uuid4

class BlockChain(object):
    ...
    def proof_of_work(self, last_proof):
        # simple proof of work algorithm
        # find a number p' such as hash(pp') containing leading 4 zeros where p is the previous p'
        # p is the previous proof and p' is the new proof
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1
        return proof
    
    @staticmethod
    def validate_proof(last_proof, proof):
        # validates the proof: does hash(last_proof, proof) contain 4 leading zeroes?
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"
```

To adjust the difficulty of the algorithm, we could modify the number of leading zeors.  But strictly speaking 4 is sufficient enough.  Also, you may find out that adding an extra 0 makes a mammoth difference to the time required to find a solution.

Now, our Blockchain class is pretty much complete, let's begin to interact with the ledger using the HTTP requests.


# Step 2: Blockchain as an API

We'll use Python Flask framework.  It's a micro-framework and it's really easy to use so for our example it'll do nicely.

We'll create three simple API endpoints:

  - /transactions/new to create a new transaction block
  - /mine to tell our service to mine a new block
  - /chain to return the full Blockchain

### Setting up Flask

Our server will form a single node in our Blockchain.  So let's create some code.

```python
import hashlib
import json
from time import time
from uuid import uuid4

from flask import Flask, jsonify, request

# initiate the node
app = Flask(__name__)
# generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')
# initiate the Blockchain
blockchain = BlockChain()

@app.route('/mine', methods=['GET'])
def mine():
    return "We will mine a new block"

@app.route('/transaction/new', methods=['GET'])
def transaction_new():
    return "We will add a new transaction"

@app.route('/chain', methods=['GET'])
def chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', 5000)
```

### The transaction endpoint

This is what the request for the transaction will look like. It's what the user will send to the server.

```json
{
    "sender": "sender_address",
    "recipient": "recipient_address",
    "amount": 100
}
```

Since we already have the method for adding transactions to a block, the rest is easy and pretty straight forward.

```python
import hashlib
import json

from time import time
from uulib import uulib4
from flask import Flask, jsonify, request

...

@app.route('/transactions/new', methods=['POST'])
def new_transaction():

    values = request.get_json()
    required = ['sender', 'recipient', 'amount']

    if not all(k in values for k in required):
        return 'Missing values', 400

    # create a new transaction
    index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])
    response = {'message': f'Transaction will be added to the Block {index}.'}

    return jsonify(response, 200)
```

### The mining endpoint

Our mining endpoint is where the mining happens and it's actually very easy as all it has to do are three things:

1) Calculate proof of work

2) Reward the miner by adding a transaction granting miner 1 coin

3) Forge the new Block by adding it to the chain


So, let's add on the mining function on our API:

```python
import hashlib
import json

from time import time
from uulib import uulib4
from flask import Flask, jsonify, request

...

@app.route('/mine', methods=['GET'])
def mine():

    # first we have to run the proof of work algorithm to calculate the new proof..
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)

    # we must receive reward for finding the proof
    blockchain.new_transaction(
        sender=0,
        recipient=node_identifier,
        amount=1,
    )

    # forge the new block by adding it to the chain
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)

    response = {
        'message': "Forged new block.",
        'index': block['index'],
        'transactions': block['transaction'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }
    return jsonify(response), 200
```

At this point, we are done, and we can start interacting with out blockchain.  :)


# Step 3: Interacting with our Blockchain

You can use a plain old cURL or Postman to interact with our Blockchain API ovet the network.

Fire up the server:

```
$ python3 blockchain.py
* Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)

```

So first off let's try mining a block by making a GET request to the "mine" http://localhost:5000/mine:

```json
[
  {
    "index": 1, 
    "message": "Forged new block.", 
    "previous_hash": "7cd122100c9ded644768ccdec2d9433043968352e37d23526f63eefc65cd89e6", 
    "proof": 35293, 
    "transactions": [
      {
        "data": 1, 
        "recipient": "6a01861c7b3f483eab90727e621b2b96", 
        "sender": 0
      }
    ]
  }, 
  200
]
```

Motherfucker, very good! :)

Now lets create a new transaction by making a POST request to http://localhost:5000/transaction/new with a body containing our transaction structure. Let's make this call using the cURL:

```
$ curl -X POST -H "Content-Type: application/json" -d '{
 "sender": "d4ee26eee15148ee92c6cd394edd974e",
 "recipient": "recipient-address",
 "amount": 5
}' "http://localhost:5000/transactions/new"
```

I have restarted the server, mined two blocks, to give 3 in total.  So let's inspect the full chain by requesting http://localhost:5000/chain:

```json
{
  "chain": [
    {
      "index": 1,
      "previous_hash": 1,
      "proof": 100,
      "timestamp": 1506280650.770839,
      "transactions": []
    },
    {
      "index": 2,
      "previous_hash": "c099bc...bfb7",
      "proof": 35293,
      "timestamp": 1506280664.717925,
      "transactions": [
        {
          "amount": 1,
          "recipient": "8bbcb347e0631231...e152b",
          "sender": "0"
        }
      ]
    },
    {
      "index": 3,
      "previous_hash": "eff91a...10f2",
      "proof": 35089,
      "timestamp": 1506280666.1086972,
      "transactions": [
        {
          "amount": 1,
          "recipient": "9e2e234e12e0631231...e152b",
          "sender": "0"
        }
      ]
    }
  ],
  "length": 3
}
```

# Step 4: Transaction verification

For this we will be using Python NaCl to generate a public/private signing key pair: private.key, public.key which need to be generated before runtime. We will employ the cryptography using the Public-key signature standards X.509 for Public Key Certificates.


# Step 5: Smart wallet

This is very cool. Wallet is a gateway to decentralized applications on the Blockchain. It allows you to hold and secure tokens and other crypto-assets. This Blockchain example is built on ERC-20 standards and therefore should be compatible and working out of the box with your regular wallet. :)


# Step 6: Consensus

This is very cool actually. We've got a fully valid basic Blockchain that accepts transactions and allows us to mine a new block (and get rewarded for it).  But the whole point of Blockchains is to be decentralized, and how on earth do we ensure that all the data reflect the same chain?  Well, it's actually a well know problem of Consensus, and we are going to have to implement a Consensus Algorithm if we want more that a single node in our network. So better buckle up, we're moving onto registering the new nodes. :)

### Registering new Nodes

OK, first off, before you start adding new nodes you'd need to let your node to know about his neighbouring nodes.  This needs to be done before you even start implementing Consensus Algorithm.  Each node on our network needs to keep registry of other nodes on the network.  And therefore we will need to add more endpoints to orchestrate our miner nodes:

  - /miner/register - to register a new miner node into the operation
  - /miner/nodes/resolve - to implement our consensus algorithm to resolve any potential conflicts, making sure all nodes have the correct and up to date chain

First we're goint to modify the Blockchain class constructor and add in the method for registering nodes:


```python
...
from urllib.parse import urlparse
...

class BlockChain(object):
    def __init__(self):
        ...
        self.nodes = set()
        ...
        
    def register_miner_node(self, address):
        # add on the new miner node onto the list of nodes
        parsed_url = urlparse(address)
        self.nodes.add(parse_url.netloc)
        return
```

### Implementing the Consensus Algorithm

As mentioned, conflict is when one node has a different chain to another node. To resolve this, we'll make the rule that the longest valid chain is authoritative.  In other words, the longest valid chain is de-facto one.  Using this simple rule, we reach Consensuns amongs the nodes in our network.

```python
import requests
...
class BlockChain(object):
    ...
    def valid_chain(self, chain):
        
        # determine if a given blockchain is valid
        last_block = chain[0]
        current_index = 1
        
        while current_index < len(chain):
            block = chain[current_index]
            # check that the hash of the block is correct
            if block['previous_hash'] != self.hash(last_block)
                return False
            # check that the proof of work is correct
            if not self.valid_proof(last_block['proof'], block['proof'])
                return False
        
            last_block = block
            current_index += 1

        return True

    def resolve_conflicts(self):
        # this is our Consensus Algorithm, it resolves conflicts by replacing
        # our chain with the longest one in the network.

        neighbours = self.nodes
        new_chain = None

        # we are only looking for the chains longer than ours
        max_length = len(self.chain)

        # grab and verify chains from all the nodes in our network
        for node in neighbours:

            # we utilize our own api to construct the list of chains :)
            response = request.get(f'http://{node}/chain')

            if response.status_code == 200:

                length = response.json()['length']
                chain = response.json()['chain']
                
                # check if the chain is longer and whether the chain is valid
                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    new_chain = chain
        
        # replace our chain if we discover a new longer valid chain
        if new_chain:
            self.chain = new_chain
            return True

        return False
```

OK so the first method the valid_chain loops through each block and checks that the chain is valid by verifying both the hash and the proof.

The resolve_conflicts method loops through all the neighbouring nodes, downloads their chain and verify them using the above valid_chain method.  If a valid chain is found, and it is longer than ours, we replace our chain with this new one.

So, what is left are the very last two API endpoints, specifically one for adding a neighbouring node and another for resolving the conflicts, and it's quite straight forward:

```python
@app.route('/miner/register', method=['POST'])
def register_new_miner():
    values = request.get_json()
    
    # get the list of miner nodes
    nodes = values.get('nodes')
    if nodes is None: 
        return "Error: Please supply list of valid nodes", 400

    # register nodes
    for node in nodes:
        blockchain.register_node(node)
        
    response = {
        'message': 'New nodes have been added.',
        'total_nodes': list(blockchain.nodes),
    }
    return jsonify(response), 200

@app.route('/miner/nodes/resolve', method=['POST'])
def consensus():
    # an attempt to resolve conflicts to reach the consensus
    conflicts = blockchain.resolve_conflicts()
    
    if(conflicts):
        response = {
            'message': 'Our chain was replaced.',
            'new_chain': blockchain.chain,
        }
        return jsonify(response), 200
    
    response = {
        'message': 'Our chain is authoritative.',
        'chain': blockchain.chain,
    }
    return jsonify(response), 200
```

And here comes the big one, the one you have been waiting for as at this point you can grab a different machine or a computer if you like and spin up different miners on our network. :)  

Or you can run multiple miners on your single machine by running the same process but using a different port number.
As an example, I can run another miner node on my machine by running it on a different port and register it with the current miner. Therefore I have two miners: http://localhost:5000 and http://localhost:5001.

### Registering a new node

```
$ curl -X POST -H "Content-Type: application/json" -d '{
 "nodes": ["http://127.0.0.1:5001"],
}' "http://localhost:5000/nodes/register"
```

Request OK, returned:
```json
{
    "message": "New nodes have been added.",
    "all_nodes": [
        "127.0.0.1:5001"
    ]
}
```

### Consensus Algorithm at Work

```
$ curl http://localhost:5000/nodes/resolve"
```

Request OK, returns:

```json
{
    "message": "Our chain was replaced.",
    "new_chain": [
        {
            "index": 1,
            "previous_hash": 1,
            "proof": 100,
            "timestamp": 1525160363.12144,
            "transactions": [],
        },
        {
            "index": 2,
            "previous_hash": "7cd122100c9ded644768ccdec2d9433043968352e37d23526f63eefc65cd89e6",
            "proof": 35293,
            "timestamp": 1525160706.82745,
            "transactions": [
             {
                 "amount": 1,
                 "recipient": "a77f5cdfa2934hv25c7c7da5df1f",
                 "sender": 0,
             }
            ]
        },
    ]
}
```

And that's a wrap... Now go get some friends to mine your Blockchain. :)


License
----

BSD-2-Clause


### Donation Address

ETH: 0xbcFAB06E0cc4Fe694Bdf780F1FcB1bB143bD93Ad

Have fun! :)

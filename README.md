# Blockchain

Simple Blockchain implementation written in Python.

Understanding blockchain isn't easy. At least it wasn't for me. I had to go through number of frustrations due to too few funcional examples of how this technology works. And I like learning by doing so if you do the same, allow me to guide you and by the end you will have a functioning Blockchain with a solid idea of how they work.

### Before you get started..

Remember that a blockchain is an immutable, sequential chain of records called Blocks. They can contain transactions, files or any data you like, really. But the important thing is that they’re chained together using hashes.

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

We'll create a blockchain class whose constructor creates a list to store our blockchain and another to store transactions.  Here is how the Class will look like:

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
class Blockchain(object):
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

xxx


# Step 2: Blockchain as an API

xxx


# Step 3: Interacting with our blockchain

xxx


# Step 4: Consensus


xxx


# Step 5: Transaction verification

For this we will be using Python NaCl to generate a public/private signing key pair: private.key, public.key which need to be generated before runtime.

We will employ the cryptography using the Public-key signature standards X.509 for Public Key Certificates.

For more information on the X.509 please refer to the X.509 documentation.  More on that here https://en.wikipedia.org/wiki/X.509    



# Step 5: Issuing coins for our blockchain

xxx


# Step 6: Basic contracts (P2P Protocol)

xxx




License
----

BSD-2-Clause

**Free Software, Hell Yeah!**

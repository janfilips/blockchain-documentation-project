import hashlib
import json
import time

class BlockChain(object):
    """ Main BlockChain class """
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
        # creates a new block in the blockchain
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

    def full_chain(self):
        # returns the full chain and a number of blocks
        pass

    def new_transaction(self, sender, recipient, amount):
        # adds a new transaction into the list of transactions
        # these transactions go into the next mined block
        self.current_transactions.append({
            "sender":sender,
            "recient":recipient,
            "data":amount,
        })
        return int(self.last_block['index'])+1

class BlockChain(object):
    """ Main BlockChain class """
    def __init__(self):
        self.chain = []
        self.current_transactions = []

    @staticmethod
    def hash(block):
        # hashes a block
        pass

    def new_block(self):
        # creates a new block and adds it on the chain
        pass

    @property
    def last_block(self):
        # returns last block in the chain
        return self.chain[-1]

    def full_chain(self):
        # returns the full chain and a number of blocks
        pass

    def add_new_transaction(self, sender, recipient, data):
        # adds a new transaction into the list of transactions
        # these transactions go into the next mined block
        self.current_transactions.append({
            "sender":sender,
            "recient":recipient,
            "data":data,
        })
        return int(self.last_block['index'])+1

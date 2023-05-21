import hashlib
import time

class Transaction:
    def __init__(self, sender, receiver, amount):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount

class Block:
    def __init__(self, index, timestamp, transactions, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        sha = hashlib.sha256()
        sha.update(str(self.index).encode('utf-8') +
                   str(self.timestamp).encode('utf-8') +
                   str(self.transactions).encode('utf-8') +
                   str(self.previous_hash).encode('utf-8'))
        return sha.hexdigest()


class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.pending_transactions = []

    def create_genesis_block(self):
        return Block(0, time.time(), [], "0")

    def get_latest_block(self):
        return self.chain[-1]

    def mine_pending_transactions(self, mining_reward_address):
        block = Block(len(self.chain), time.time(), self.pending_transactions, self.get_latest_block().hash)
        self.chain.append(block)
        self.pending_transactions = []
        self.pending_transactions.append(Transaction(None, mining_reward_address, 1))  # Reward for mining

    def create_transaction(self, sender, receiver, amount):
        self.pending_transactions.append(Transaction(sender, receiver, amount))

    def get_balance(self, address):
        balance = 0
        for block in self.chain:
            for transaction in block.transactions:
                if transaction.sender == address:
                    balance -= transaction.amount
                if transaction.receiver == address:
                    balance += transaction.amount
        return balance


# Usage example
blockchain = Blockchain()
miner_address = "Miner Address"

blockchain.create_transaction("Address1", "Address2", 5)
blockchain.create_transaction("Address2", "Address1", 2)

blockchain.mine_pending_transactions(miner_address)

balance_address1 = blockchain.get_balance("Address1")
balance_address2 = blockchain.get_balance("Address2")
balance_miner = blockchain.get_balance(miner_address)

print("Balance of Address1:", balance_address1)
print("Balance of Address2:", balance_address2)
print("Balance of Miner Address:", balance_miner)

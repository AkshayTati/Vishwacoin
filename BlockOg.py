import hashlib
import time

class Transaction:
    def __init__(self, sender, recipient, amount):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount

class Block:
    def __init__(self, index, timestamp, transactions, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        data_string = (
            str(self.index)
            + str(self.timestamp)
            + str(self.transactions)
            + str(self.previous_hash)
            + str(self.nonce)
        )
        return hashlib.sha256(data_string.encode()).hexdigest()

    def mine_block(self, difficulty, miner_address, mining_reward):
        target = "0" * difficulty

        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()

        self.transactions.append(Transaction(None, miner_address, mining_reward))

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.difficulty = 4
        self.pending_transactions = []
        self.mining_reward = 100
        self.wallets = {}

    def create_genesis_block(self):
        return Block(0, time.time(), [], "0")

    def get_latest_block(self):
        return self.chain[-1]

    def add_transaction(self, transaction):
        self.pending_transactions.append(transaction)

    def mine_pending_transactions(self, miner_address):
        block = Block(
            len(self.chain),
            time.time(),
            self.pending_transactions,
            self.get_latest_block().hash,
        )
        block.mine_block(self.difficulty, miner_address, self.get_mining_reward())
        self.chain.append(block)

        self.pending_transactions = []

    def get_balance(self, address):
        if address in self.wallets:
            return self.wallets[address]
        else:
            return 0

    def create_wallet(self, initial_balance=0):
        new_wallet_address = hashlib.sha256(str(time.time()).encode()).hexdigest()
        self.wallets[new_wallet_address] = initial_balance
        return new_wallet_address

    def execute_transaction(self, sender_address, recipient_address, amount):
        if sender_address not in self.wallets or recipient_address not in self.wallets:
            print("Invalid sender or recipient address.")
            return

        sender_balance = self.get_balance(sender_address)
        if sender_balance < amount:
            print("Insufficient funds in the sender's wallet.")
            return

        transaction = Transaction(sender_address, recipient_address, amount)
        self.add_transaction(transaction)
        self.wallets[sender_address] -= amount
        self.wallets[recipient_address] += amount

        print("Transaction added to pending transactions.")

    def get_mining_reward(self):
        num_transactions = len(self.pending_transactions)
        return self.mining_reward + num_transactions

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            # Check if the current block is valid
            if not current_block.is_valid():
                return False

            # Check if the previous hash is correct
            if current_block.previous_hash != previous_block.hash:
                return False

        return True

    def get_transaction_history(self, wallet_address):
        transaction_history = []

        for block in self.chain:
            for transaction in block.transactions:
                if transaction.sender == wallet_address or transaction.recipient == wallet_address:
                    transaction_history.append(transaction)

        return transaction_history


    def get_balance_history(self, wallet_address):
        balance_history = []

        for block in self.chain:
            block_balance = {}
            for transaction in block.transactions:
                if transaction.sender == wallet_address:
                    block_balance[transaction.sender] = block_balance.get(transaction.sender, 0) - transaction.amount
                if transaction.recipient == wallet_address:
                    block_balance[transaction.recipient] = block_balance.get(transaction.recipient, 0) + transaction.amount
            balance_history.append((block.timestamp, block_balance))

        return balance_history

# Usage example
blockchain = Blockchain()
alice_wallet = blockchain.create_wallet(initial_balance=200)
bob_wallet = blockchain.create_wallet(initial_balance=50)

print("Alice's balance:", blockchain.get_balance(alice_wallet))
print("Bob's balance:", blockchain.get_balance(bob_wallet))

blockchain.execute_transaction(alice_wallet, bob_wallet, 30)
blockchain.execute_transaction(alice_wallet, bob_wallet, 50)

blockchain.mine_pending_transactions(alice_wallet)

print("Alice's balance:", blockchain.get_balance(alice_wallet))
print("Bob's balance:", blockchain.get_balance(bob_wallet))

# transaction_history = blockchain.get_transaction_history(alice_wallet)

# print("Transaction history for Alice's wallet:")
# for transaction in transaction_history:
#     print("Sender:", transaction.sender)
#     print("Recipient:", transaction.recipient)
#     print("Amount:", transaction.amount)
#     print("------------------")


# balance_history = blockchain.get_balance_history(alice_wallet)

# print("Balance history for Alice's wallet:")
# for timestamp, balance in balance_history:
#     print("Timestamp:", timestamp)
#     print("Balance:", balance.get(alice_wallet, 0))
#     print("------------------")
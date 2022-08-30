from datetime import datetime
from block import Block
import transactionException
from transaction import Transaction

class BlockChain:
    def __init__(self):
        self.timestamp = datetime.now()
        self.blocks = list()


    def add_block_to_chain(self,a_block):
        if isinstance(a_block,Block):
            if len(self.blocks) > 0 : a_block.prev_block_hash = self.blocks[-1].block_hash
            a_block.seal_block()
            a_block.validate_block()
            self.blocks.append(a_block)
        else:
            raise ValueError("argument is not of type Block")

    def validate_chain(self):
        for index, block in enumerate(self.blocks):
            try:
                block.validate_block()
            except transactionException.BlockException as bfe:
                raise transactionException.BlockChainException\
                    ("Blockchain creation failed due to block number = " + index + str(bfe))

# Question 3:
    def add_transaction_to_queue(self, transaction):
        if isinstance(transaction, Transaction):
            if len(self.unverified_transactions) > 0:
                transaction.link_transactions(self.unverified_transactions[-1])
            transaction.seal()
            # check that there is no tempering between seal() and appending the transaction
            transaction.validate_integrity()
            if transaction.sender.validate_enough_tokens(transaction.message.amount):
                self.unverified_transactions.append(transaction)
                transaction.sender.subtract_tokens(transaction.message.amount)
                transaction.receiver.add_tokens(transaction.message.amount)
            else:
                raise transactionException("you don't have enough tokens")

from datetime import datetime
import hashlib
from transaction import Transaction
from transactionException import TransactionException
from transactionException import BlockException
from typing import Callable, List
import dataclasses as dc
import Message

class Block:
    prev_block_hash: str
    index: int
    messages: List[Message]
    current_block_hash: str = dc.field(init=False)
    time_added: datetime = dc.field(init=False)
    nonce: int = dc.field(init=False)

    TOKEN_PRIZE = 3


    def __init__(self,*transactions):
        """
        :param transactions: an unknown number of Transaction objects
        """
        self.transactions = list()
        if transactions:
            if all(isinstance(a_transaction,Transaction) for a_transaction in transactions):
                self.transactions.extend(transactions)
        self.timestamp = None
        self.block_hash = None
        self.prev_block_hash = None

    def add_transaction(self,transaction):
        if isinstance(transaction, Transaction):
            if len(self.transactions) > 0:
                transaction.link_transactions(self.transactions[-1])
            transaction.seal()
            # check that there is no tempering between seal() and appending the transaction
            transaction.validate_integrity()
            self.transactions.append(transaction)

    def compute_block_hash(self):
        block_hash_str = str(self.timestamp) + str(self.prev_block_hash) + self.transactions[-1].trans_hash
        members_bytearray = bytearray(block_hash_str, encoding="utf-8")
        return hashlib.sha256(members_bytearray).hexdigest()

    def link_to_prev_block(self,prev_block):
        if isinstance(prev_block,Block):
            self.prev_block_hash = prev_block.block_hash
        else:
            raise ValueError("argument is not of Block type")
        """
        Iterate over the transactions, and try to validate each transaction
        if validation fails, possibly except TemperedTransaction
        """

    def seal_block(self):
        self.timestamp = datetime.now()
        self.block_hash = self.compute_block_hash()


# Question 1:
    def validate_single_block(self):
        """
        1. validate integrity of each transaction
        2. validate integrity of chain of transactions
        :return:
        """
        for index, transaction in enumerate(self.transactions):
            try:
                transaction.validate_integrity()
                if index > 0 and transaction.prev_trans_hash != self.transactions[index-1].trans_hash:
                    raise BlockException("Block creation failed due linking problem in transaction number: "
                                         + index)
            except TransactionException as tte:
                raise BlockException("Block creation failed due to validation problem in transaction number: "
                                     + index + str (tte))













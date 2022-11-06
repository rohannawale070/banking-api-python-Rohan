import unittest

from models.transaction import TransactionModel


def test_find_by_acc_number():
    response = [
        {
            "acc_number": 2,
            "amount": 50,
            "transaction_id": 1,
            "transaction_type": "Amount Transferred to account number: 1",
            "created_at": "22-10-26 21:16:37"
        },
        {
            "acc_number": 2,
            "amount": 50,
            "transaction_id": 3,
            "transaction_type": "Amount Transferred to account number: 1",
            "created_at": "22-10-26 21:52:05"
        }
    ]
    tm = TransactionModel(acc_number=2,
                          amount=50,
                          transaction_type="Amount Transferred to account number: 1",
                          created_at='2022-10-26')
    assert tm.find_by_acc_number(2) == response

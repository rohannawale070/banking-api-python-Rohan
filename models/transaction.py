from typing import List
from bank_database import bankDatabase


class TransactionModel(bankDatabase.Model):
    __tablename__ = "transactions"
    transaction_id = bankDatabase.Column(bankDatabase.Integer, primary_key=True, autoincrement=True)
    acc_number = bankDatabase.Column(bankDatabase.Integer, bankDatabase.ForeignKey('accounts.acc_number'))
    amount = bankDatabase.Column(bankDatabase.REAL, nullable=False)
    transaction_type = bankDatabase.Column(bankDatabase.String(250))
    created_at = bankDatabase.Column(bankDatabase.String(250))

    def __init__(self, acc_number: int, amount: float, transaction_type: str, created_at: str):
        self.acc_number = acc_number
        self.amount = amount
        self.transaction_type = transaction_type
        self.created_at = created_at

    @classmethod
    def find_by_acc_number(cls, acc_number: int) -> List["TransactionModel"]:
        return cls.query.filter_by(acc_number=acc_number).all()

    def save_to_db(self) -> None:
        bankDatabase.session.add(self)
        bankDatabase.session.commit()

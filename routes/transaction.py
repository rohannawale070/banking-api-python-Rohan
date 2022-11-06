from datetime import datetime

from flask import request, flash
from flask_restplus import Resource, fields, Namespace

from bank_database import bank_db
from schemas.transaction import TransactionSchema
from models.transaction import TransactionModel

TRANSACTION_NOT_FOUND = "Transaction not found."
TRANSFER_SUCCESSFUL = "Transaction successful."

make_transaction = Namespace('MakeTransaction', description='Transfer amounts between two accounts')
get_transactions = Namespace('GetTransaction', description='Retrieve transfer history for a given account')

transaction_schema = TransactionSchema()
transactions_schema = TransactionSchema(many=True)


# flask_restplus expected Model
transaction = make_transaction.model('Transaction', {
    'from_acc_number': fields.Integer,
    'to_acc_number': fields.Integer,
    'amount': fields.Float,
})


# Retrieve transfer history for a given account
class GetTransaction(Resource):
    @get_transactions.doc('Get all transactions')
    def get(self, acc_number: int) -> tuple:
        transaction_data = TransactionModel.find_by_acc_number(acc_number)
        if not transaction_data:
            return {'message': TRANSACTION_NOT_FOUND}, 404
        return transactions_schema.dump(TransactionModel.find_by_acc_number(acc_number)), 200


# Transfer amounts between any two accounts, including those owned by different customers.
class Transaction(Resource):
    @make_transaction.expect(transaction)
    def put(self) -> tuple:
        # Get request body json
        transaction_json = request.get_json()
        transfer_amount = transaction_json['amount']
        if transaction_json['from_acc_number'] != transaction_json['to_acc_number']:
            from_acc_details = bank_db.execute("Select * from accounts where acc_number = :from_acc_number",
                                               {"from_acc_number": transaction_json['from_acc_number']}).fetchone()

            to_acc_details = bank_db.execute("Select * from accounts where acc_number = :to_acc_number",
                                             {"to_acc_number": transaction_json['to_acc_number']}).fetchone()
            # Check if from and to both the accounts exists
            if from_acc_details is not None and to_acc_details is not None:
                # Check if sender has sufficient balance in account
                if from_acc_details.balance > transfer_amount:
                    # Calculate balance after every transaction
                    source_balance = from_acc_details.balance - transfer_amount
                    target_balance = to_acc_details.balance + transfer_amount

                    # Update sender's account balance after transaction
                    bank_db.execute("update accounts set balance = :balance where cust_id = "
                                    ":cust_id and acc_number = :acc_number",
                                    {"balance": source_balance,
                                     "cust_id": from_acc_details.cust_id,
                                     "acc_number": from_acc_details.acc_number})
                    bank_db.commit()

                    # Insert transaction entry into transactions table for sender
                    source_transaction = TransactionModel(acc_number=from_acc_details.acc_number,
                                                          amount=transfer_amount,
                                                          transaction_type="Amount Transferred to account number: " + str(to_acc_details.acc_number),
                                                          created_at=datetime.today().strftime('%y-%m-%d %H:%M:%S'))
                    bank_db.add(source_transaction)
                    bank_db.commit()

                    # Update receiver's account balance after transaction
                    bank_db.execute("update accounts set balance = :balance where cust_id = "
                                    ":cust_id and acc_number = :acc_number",
                                    {"balance": target_balance,
                                     "cust_id": to_acc_details.cust_id,
                                     "acc_number": to_acc_details.acc_number})
                    bank_db.commit()

                    # Insert transaction entry into transactions table for receiver
                    target_transaction = TransactionModel(acc_number=to_acc_details.acc_number,
                                                          amount=transfer_amount,
                                                          transaction_type="Amount received from account number: " + str(from_acc_details.acc_number),
                                                          created_at=datetime.today().strftime('%y-%m-%d %H:%M:%S'))
                    bank_db.add(target_transaction)
                    bank_db.commit()
                else:
                    return {'message': "Insufficient balance"}, 404
            else:
                return {'message': "Account not found"}, 404
        else:
            return {'message': "Transfer cant be made to same account"}, 404
        return {'message': TRANSFER_SUCCESSFUL}, 200

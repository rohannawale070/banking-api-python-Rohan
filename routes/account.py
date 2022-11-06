from flask import request
from flask_restplus import Resource, fields, Namespace

from bank_database import bank_db
from models.account import AccountModel
from schemas.account import AccountSchema
from datetime import datetime
from itertools import chain

ACCOUNT_NOT_FOUND = "Account not found."

get_account = Namespace('GetAccount', description='Retrieve balances for a given account')
create_account = Namespace('CreateAccount', description='Create a new bank account for a customer')

account_schema = AccountSchema()

# flask_restplus expected Model
account = get_account.model('Account', {
    'tax_id_number': fields.Integer,
    'first_name': fields.String,
    'last_name': fields.String,
    'acc_type': fields.String,
    'initial_deposit_amount': fields.Float
})


# Retrieve balances for a given account.
class GetAccount(Resource):
    # Show balance for given Account
    def get(self, acc_number: int) -> tuple:
        account_data = AccountModel.find_by_acc_number(acc_number)
        if not account_data:
            return {'message': ACCOUNT_NOT_FOUND}, 404
        return account_schema.dump(account_data), 200


# Create a new bank account for a customer, with an initial deposit amount. A single customer may have multiple bank accounts.
class CreateAccount(Resource):
    @create_account.expect(account)
    def put(self) -> tuple:
        # Get request body json
        account_json = request.get_json()
        account_json['balance'] = account_json.pop('initial_deposit_amount')
        input_tax_id_number = account_json['tax_id_number']

        # Check is customer already exists for given tax_id_number
        existing_customer = bank_db.execute("SELECT * FROM accounts where tax_id_number = :tax",
                                            {"tax": input_tax_id_number}).fetchone()
        if existing_customer is not None:
            # Get list of account types of the existing customer
            existing_cust_acc_types = bank_db.execute("SELECT acc_type FROM accounts where tax_id_number = :tax",
                                                      {"tax": input_tax_id_number}).fetchall()
            existing_cust_acc_types = list(chain(*existing_cust_acc_types))
            # Check if customer is having same type of account already
            if account_json['acc_type'] in existing_cust_acc_types:
                return {'message': "Customer already has already same type of account"}, 403
            else:
                # Keep cust_id same to create different type of account for the existing customer
                account_json['cust_id'] = existing_customer.cust_id
        else:
            # Auto-increment of the cust_id for new customer
            cust_id = bank_db.execute("SELECT IFNULL(MAX(cust_id), 0) +1 as new_cust_id FROM accounts").fetchone()
            account_json['cust_id'] = cust_id.new_cust_id
        # Add timestamp for the creation or update of the account
        account_json['created_at'] = datetime.today().strftime('%y-%m-%d %H:%M:%S')

        account_data = account_schema.load(account_json)
        account_data.save_to_db()
        return account_schema.dump(account_data), 200

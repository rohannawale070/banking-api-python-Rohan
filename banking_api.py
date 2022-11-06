from flask import Flask, Blueprint, jsonify
from flask_restplus import Api
from flask_sqlalchemy_integrate import ma
from bank_database import bankDatabase
from routes.account import GetAccount, get_account, create_account, CreateAccount
from marshmallow import ValidationError
from routes.transaction import Transaction, make_transaction, get_transactions, GetTransaction

bankingAppInstance = Flask(__name__)

bluePrint = Blueprint('api', __name__, url_prefix='/api')
bankingApi = Api(bluePrint, doc='/doc', title='Internal Banking API')
bankingAppInstance.register_blueprint(bluePrint)

bankingAppInstance.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
bankingAppInstance.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
bankingAppInstance.config['PROPAGATE_EXCEPTIONS'] = True

bankingApi.add_namespace(create_account)
bankingApi.add_namespace(get_account)
bankingApi.add_namespace(make_transaction)
bankingApi.add_namespace(get_transactions)


# Add routes for API endpoints
create_account.add_resource(CreateAccount, "")
get_account.add_resource(GetAccount, '/<int:acc_number>')
make_transaction.add_resource(Transaction, "")
get_transactions.add_resource(GetTransaction, '/<int:acc_number>')


@bankingAppInstance.before_first_request
def create_tables():
    bankDatabase.create_all()


@bankingApi.errorhandler(ValidationError)
def handle_validation_error(error):
    return jsonify(error.messages), 400


if __name__ == '__main__':
    bankDatabase.init_app(bankingAppInstance)
    ma.init_app(bankingAppInstance)
    bankingAppInstance.run(host="0.0.0.0", port=8000, debug=True, use_reloader=True)

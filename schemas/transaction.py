from flask_sqlalchemy_integrate import ma
from models.transaction import TransactionModel


class TransactionSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = TransactionModel
        load_instance = True
        include_fk = True

from flask_sqlalchemy_integrate import ma
from models.account import AccountModel


class AccountSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = AccountModel
        load_instance = True
        include_fk = True

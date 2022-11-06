from bank_database import bankDatabase


class AccountModel(bankDatabase.Model):
    __tablename__ = "accounts"
    acc_number = bankDatabase.Column(bankDatabase.Integer, primary_key=True, autoincrement=True)
    tax_id_number = bankDatabase.Column(bankDatabase.Integer, nullable=False)
    cust_id = bankDatabase.Column(bankDatabase.Integer, nullable=False)
    first_name = bankDatabase.Column(bankDatabase.String(250), nullable=False)
    last_name = bankDatabase.Column(bankDatabase.String(250), nullable=False)
    acc_type = bankDatabase.Column(bankDatabase.String(250), nullable=False)
    balance = bankDatabase.Column(bankDatabase.REAL, nullable=False)
    created_at = bankDatabase.Column(bankDatabase.String(250))

    def __init__(self, tax_id_number: int, cust_id: int, first_name: str, last_name: str, acc_type: str, balance: float, created_at: str):
        self.tax_id_number = tax_id_number
        self.cust_id = cust_id
        self.first_name = first_name
        self.last_name = last_name
        self.acc_type = acc_type
        self.balance = balance
        self.created_at = created_at

    @classmethod
    def find_by_acc_number(cls, acc_number: int) -> "AccountModel":
        return cls.query.filter_by(acc_number=acc_number).first()

    def save_to_db(self) -> None:
        bankDatabase.session.add(self)
        bankDatabase.session.commit()

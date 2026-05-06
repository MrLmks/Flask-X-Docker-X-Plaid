from app import db

class Transaction(db.Model):
    __tablename__ = "transactions"

    id = db.Column(db.Integer, primary_key=True)

    transaction_id = db.Column(db.String(255), unique=True, nullable=False)
    amount = db.Column(db.Float, unique=False, nullable=False)
    date = db.Column(db.Date, nullable=False)
    billing_entity = db.Column(db.String(255), unique=False, nullable=False)
    category = db.Column(db.String(255), unique=False, nullable=False)
    currency = db.Column(db.String(255), unique=False, nullable=False)

    def __repr__(self):
        return f"<Transaction {self.transaction_id} - {self.amount} {self.currency}>"
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
    
class Token(db.Model):
    __tablename__ = "tokens"

    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.String(255), nullable=False)
    # Doesn't need to be unique as user with mutiple bank accounts will share the same ID
    client_user_id = db.Column(db.String(255), nullable=False)
    creation_date = db.Column(db.DateTime, default=db.func.current_timestamp())
    access_token = db.Column(db.String(255), unique=True, nullable=False)
    
    def __repr__(self):
        return f"<Token {self.client_user_id}>"


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)

    def __repr__(self):
        return f"Welcome {self.username} !"

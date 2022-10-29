from db import db


class WalletModel(db.Model):
    __tablename__ = 'wallets'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    currency = db.Column(db.String(80), nullable=False)
    balance = db.Column(db.Float(precision=2), nullable=False)
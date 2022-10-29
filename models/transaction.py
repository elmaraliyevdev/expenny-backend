from db import db


class TransactionModel(db.Model):
    __tablename__ = 'transactions'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    category = db.relationship('CategoryModel', uselist=False)
    category_id = db.Column(db.Integer, db.ForeignKey('resources.id'), nullable=False)
    date = db.Column(db.String(80), nullable=False)
    amount = db.Column(db.Float(precision=2), nullable=False)
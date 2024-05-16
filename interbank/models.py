from datetime import datetime
from interbank import db,login_manager
from flask_login import UserMixin
from sqlalchemy import Sequence

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, Sequence('user_account_id_seq', start=1000), primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    bank_name = db.Column(db.String(20), nullable=False)
    account_type = db.Column(db.String(20), nullable=False)
    balance_amount = db.Column(db.Float,nullable=False)

class Transfer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    from_account = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
    to_account = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
    amount = db.Column(db.Float,nullable=False)


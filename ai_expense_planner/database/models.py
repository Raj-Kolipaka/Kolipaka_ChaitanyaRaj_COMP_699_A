from datetime import datetime
from database.db import db


# -------- USER TABLE --------
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default="student")  # student or admin

    # relationships
    expenses = db.relationship('Expense', backref='user', lazy=True)
    loans = db.relationship('Loan', backref='user', lazy=True)
    notifications = db.relationship('Notification', backref='user', lazy=True)


# -------- EXPENSE TABLE --------
class Expense(db.Model):
    __tablename__ = "expenses"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50))  # tuition, rent, food, travel
    date = db.Column(db.DateTime, default=datetime.utcnow)


# -------- LOAN TABLE --------
class Loan(db.Model):
    __tablename__ = "loans"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    principal = db.Column(db.Float, nullable=False)
    interest_rate = db.Column(db.Float, nullable=False)
    emi_amount = db.Column(db.Float, nullable=False)

    balance = db.Column(db.Float, nullable=False)
    total_paid = db.Column(db.Float, default=0)

    start_date = db.Column(db.DateTime, default=datetime.utcnow)


# -------- NOTIFICATION TABLE --------
class Notification(db.Model):
    __tablename__ = "notifications"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    message = db.Column(db.String(255))
    date = db.Column(db.DateTime, default=datetime.utcnow)

    is_read = db.Column(db.Boolean, default=False)
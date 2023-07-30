from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(15), nullable=False)
    profile_pic = db.Column(db.Text, nullable=True)
    gender = db.Column(db.String(6), nullable=False)
    time = db.Column(db.DateTime(timezone=True), default=func.now())
    cloths = db.relationship('Cloth')
    logs = db.relationship('Log')
    combos = db.relationship('Combination')

class Cloth(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(15), unique=True, nullable=False)
    description = db.Column(db.String(500), nullable=False)
    image = db.Column(db.Text, nullable=False)
    isCommitted = db.Column(db.Boolean, nullable=False)
    type = db.Column(db.String(6), nullable=False)
    time = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(15), default='A combo')
    event = db.Column(db.String(12), nullable=False)
    time = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Combination(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    top = db.Column(db.String(15), nullable=False)
    bottom = db.Column(db.String(15), nullable=False)
    isBlacklisted = db.Column(db.Boolean, default=False)
    time = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
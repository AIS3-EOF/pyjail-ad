from flask_sqlalchemy import SQLAlchemy
from .sandbox.checker import DEFAULT_CHECKER

db = SQLAlchemy()


class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    checker = db.Column(db.String, default=DEFAULT_CHECKER)
    flag = db.Column(db.String, default="NotFLAG{MISSING_FLAG}")
    score = db.Column(db.Integer, default=0)

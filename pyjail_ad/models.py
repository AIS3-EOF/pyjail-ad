from flask_sqlalchemy import SQLAlchemy
from .sandbox.apply_jail import DEFAULT_JAIL

db = SQLAlchemy()


class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    jail = db.Column(db.String, default=DEFAULT_JAIL)
    flag = db.Column(db.String, default="NotFLAG{MISSING_FLAG}")
    score = db.Column(db.Integer, default=0)

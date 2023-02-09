from flask_sqlalchemy import SQLAlchemy
from .sandbox.apply_jail import DEFAULT_JAIL

db = SQLAlchemy()


class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    jail = db.Column(db.String, default=DEFAULT_JAIL)
    flag = db.Column(db.String, default="NotFLAG{MISSING_FLAG}")
    score = db.Column(db.Integer, default=0)

class AttackLog(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    team_id = db.Column(db.Integer)
    target_id = db.Column(db.Integer)
    jail = db.Column(db.String)
    code = db.Column(db.String)
    new_code = db.Column(db.String)
    stdout = db.Column(db.String)
    stderr = db.Column(db.String)

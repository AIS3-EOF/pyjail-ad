from flask import Flask, request, render_template, redirect, url_for, session, jsonify
from functools import wraps
import secrets
import random
from uuid import uuid4
from .models import db, Team
from . import sandbox

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.secret_key = secrets.token_bytes(16).hex()
db.init_app(app)
with app.app_context():
    db.create_all()


@app.get("/")
def index():
    return render_template("index.html")


def rand_team():
    # for local testing
    id = random.randint(1, 2)
    team_info = {"name": f"Team {id}", "id": id}
    return team_info


@app.post("/login")
def login():
    token = request.form["token"]
    team_info = rand_team()
    team = Team.query.filter_by(id=team_info["id"]).first()
    if team is None:
        team = Team(id=team_info["id"], name=team_info["name"])
        db.session.add(team)
        db.session.commit()
    session["team_id"] = team.id
    return redirect(url_for("panel"))


def login_required(f):
    @wraps(f)
    def decor(*args, **kwargs):
        if "team_id" not in session:
            return redirect(url_for("index"))
        return f(*args, **kwargs)

    return decor


@app.get("/panel")
@login_required
def panel():
    team = Team.query.filter_by(id=session["team_id"]).first()
    teams = Team.query.all()
    return render_template("panel.html", team=team, teams=teams)


@app.get("/api/checker")
@login_required
def get_checker():
    team = Team.query.filter_by(id=session["team_id"]).first()
    return jsonify({"status": "ok", "checker": team.checker})


@app.post("/api/checker")
@login_required
def update_checker():
    team = Team.query.filter_by(id=session["team_id"]).first()
    team.checker = request.json["checker"]
    db.session.commit()
    return jsonify({"status": "ok", "message": "Checker code updated"})


@app.get("/api/teams")
def teams():
    teams = Team.query.all()
    return jsonify(
        [{"id": team.id, "name": team.name, "score": team.score} for team in teams]
    )


@app.post("/api/attack/<target>")
@login_required
def attack(target):
    code = request.json["code"]
    if not isinstance(code, str):
        return jsonify({"status": "error", "message": "code must be a string"})
    target_team = Team.query.filter_by(id=target).first()
    if target_team is None:
        return jsonify({"status": "error", "message": "target not found"})
    team = Team.query.filter_by(id=session["team_id"]).first()
    if not sandbox.check(target_team.checker, code):
        return jsonify(
            {"status": "error", "message": "failed to pass target's checker"}
        )
    flag = f"FLAG{{{uuid4()}}}"
    result = sandbox.run(
        code,
        files=[
            {
                "name": "flag.txt",
                "content": flag.encode(),
            }
        ],
    )
    resp = {
        "status": "ok",
        "exit_code": result.exit_code,
        "stdout": result.stdout.decode(),
        "stderr": result.stderr.decode(),
        "get_flag": False,
    }
    if flag in resp["stdout"]:
        team.score += 1
        db.session.commit()
        resp["get_flag"] = True
    return jsonify(resp)

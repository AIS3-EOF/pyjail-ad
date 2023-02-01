from flask import (
    Flask,
    request,
    render_template,
    redirect,
    url_for,
    session,
    jsonify,
    flash,
)
from functools import wraps
import secrets
import random
from uuid import uuid4
from .models import db, Team
from . import sandbox
from .worker.api import connect_api, CHALLENGE_ID
import os
import requests

API_HOST = os.environ.get("API_HOST", "http://localhost:8088")
api_info = {
    "api_server": API_HOST,
    "challenge_id": CHALLENGE_ID,
}

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////tmp/pyjail.db"
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.secret_key = secrets.token_bytes(16).hex()
db.init_app(app)
with app.app_context():
    db.create_all()
    for t in connect_api().teams_get():
        if Team.query.filter_by(id=t["id"]).first() is None:
            team = Team(id=t["id"], name=t["name"])
            db.session.add(team)
    db.session.commit()


@app.get("/")
def index():
    return render_template("index.html")


@app.post("/login")
def login():
    token = request.form["token"]
    team_info = requests.get(
        f"{API_HOST}/team/my", headers={"Authorization": token}
    ).json()
    if "id" not in team_info:
        flash("Login failed")
        return redirect(url_for("index"))
    team = Team.query.filter_by(id=team_info["id"]).first()
    if team is None:
        # this really shouldn't happen
        team = Team(id=team_info["id"], name=team_info["name"])
        db.session.add(team)
        db.session.commit()
    session["team_id"] = team.id
    session["token"] = token
    return redirect(url_for("panel"))


@app.get("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


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
    return render_template(
        "panel.html",
        team=team,
        teams=teams,
        api_info={**api_info, "token": session["token"], "id": session["team_id"]},
    )


@app.get("/api/checker")
@login_required
def get_checker():
    team = Team.query.filter_by(id=session["team_id"]).first()
    return jsonify({"status": "ok", "checker": team.checker})


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
        return jsonify({"status": "error", "message": "Code must be a string"})
    target_team = Team.query.filter_by(id=target).first()
    if target_team is None:
        return jsonify({"status": "error", "message": "Target not found"})
    team = Team.query.filter_by(id=session["team_id"]).first()
    if not sandbox.check(target_team.checker, code):
        return jsonify(
            {"status": "error", "message": "Failed to pass target's checker"}
        )
    result = sandbox.run(
        code,
        files=[
            {
                "name": "flag.txt",
                "content": team.flag.encode(),
            }
        ],
    )
    resp = {
        "status": "ok",
        "exit_code": result.exit_code,
        "stdout": result.stdout.decode(),
        "stderr": result.stderr.decode(),
    }
    return jsonify(resp)

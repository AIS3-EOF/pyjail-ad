from flask import (
    Flask,
    request,
    render_template,
    redirect,
    url_for,
    session,
    jsonify,
    flash,
    send_from_directory,
)
from functools import wraps
import secrets
import random
from uuid import uuid4
from .models import db, Team, AttackLog
from . import sandbox
from .worker.api import connect_api, CHALLENGE_ID
import os
import requests

API_SERVER = os.environ.get("API_SERVER", "http://localhost:8088")
PUBLIC_API_SERVER = os.environ.get("PUBLIC_API_SERVER", "http://localhost:8088")
api_info = {
    "api_server": PUBLIC_API_SERVER,
    "challenge_id": CHALLENGE_ID,
}

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DB_CONN", "sqlite:////tmp/pyjail.db"
)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.secret_key = secrets.token_bytes(16).hex()
db.init_app(app)
with app.app_context():
    db.create_all()
#     for t in connect_api(logger=app.logger).teams_get():
#         if Team.query.filter_by(id=t["id"]).first() is None:
#             team = Team(id=t["id"], name=t["name"])
#             db.session.add(team)
#     db.session.commit()


@app.get("/")
def index():
    return render_template("index.html")


@app.post("/login")
def login():
    token = request.form["token"]
    # team_info = requests.get(
    #     f"{API_SERVER}/team/my", headers={"Authorization": token}
    # ).json()
    # if "id" not in team_info:
    #     flash("Login failed")
    #     return redirect(url_for("index"))
    team = Team.query.filter_by(id=1).first()
    if team is None:
        # this really shouldn't happen
        team = Team(id=1, name='DUMMY')
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


@app.get("/api/jail")
@login_required
def get_jail():
    team = Team.query.filter_by(id=session["team_id"]).first()
    return jsonify({"status": "ok", "jail": team.jail})


@app.get("/api/teams")
def teams():
    teams = Team.query.all()
    return jsonify(
        [{"id": team.id, "name": team.name, "score": team.score} for team in teams]
    )

from pathlib import Path

PATCH_CHECK = []
for f in (Path(__file__).parent / "patch_check").iterdir():
    code = f.read_text()
    r = sandbox.run(code)
    PATCH_CHECK.append((f.name, code, r.exit_code, r.stdout, r.stderr))

def handle_check_patch(patch):
    feedback = ""
    try:
        p = patch.decode()
        res = sandbox.apply_jail_batch(p, [code for _, code, _, _, _ in PATCH_CHECK])
        for (name, code, exit_code, stdout, stderr), (allow, new_code) in zip(
            PATCH_CHECK, res
        ):
            if not allow:
                feedback = f"Your jail wrongly rejected the patch checking code.\nFilename: {name}"
                break
            r = sandbox.run(new_code)
            if r.exit_code != exit_code or r.stdout != stdout or r.stderr != stderr:
                feedback = f"Your jail changed the output of patch checking code.\nFilename: {name}"
                break
    except UnicodeDecodeError:
        feedback = "Yout patch is not a valid UTF-8 string."
    if not feedback:
        return {'success':True, 'feedback': feedback}
    else:
        return {'success':False, 'feedback': feedback}

@app.post('/api/patch')
def patch():
    f = request.files.get('file')
    patch = f.stream.read()
    r = handle_check_patch(patch)
    return jsonify(r)


def try_decode(b: bytes):
    try:
        return b.decode()
    except UnicodeDecodeError:
        return f"UnicodeDecodeError: {b!r}"


# @app.post("/api/attack/<target>")
# @login_required
# def attack(target):
#     code = request.json["code"]
#     if not isinstance(code, str):
#         return jsonify({"status": "error", "message": "Code must be a string"})
#     target_team = Team.query.filter_by(id=target).first()
#     if target_team is None:
#         return jsonify({"status": "error", "message": "Target not found"})
#     team = Team.query.filter_by(id=session["team_id"]).first()
#     sio.emit("traffic", [[team.id, target_team.id]])
#     allow, new_code = sandbox.apply_jail(target_team.jail, code)
#     if not allow:
#         return jsonify({"status": "error", "message": "Failed to pass target's jail"})
#     result = sandbox.run(
#         new_code,
#         files=[
#             {
#                 "name": "flag.txt",
#                 "content": target_team.flag.encode(),
#             }
#         ],
#     )
#     resp = {
#         "status": "ok",
#         "exit_code": result.exit_code,
#         "stdout": try_decode(result.stdout),
#         "stderr": try_decode(result.stderr),
#     }
#     atk_log = AttackLog(
#         team_id=team.id,
#         target_id=target_team.id,
#         jail=target_team.jail,
#         code=code,
#         new_code=new_code,
#         stdout=try_decode(result.stdout),
#         stderr=try_decode(result.stderr),
#     )
#     db.session.add(atk_log)
#     db.session.commit()
#     return jsonify(resp)


@app.get("/help")
def helppage():
    return render_template("help.html")


@app.get("/patch_check_example")
def patch_check_example():
    return send_from_directory("patch_check", "random_math.py")

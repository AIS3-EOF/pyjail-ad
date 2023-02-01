from .models import db, Team
from .app import app
from .worker.api import connect_worker_api, WorkerApi
from tempfile import TemporaryFile
import json
import time
import logging

logging.root.setLevel(logging.INFO)


def poll_jobs(api: WorkerApi, team_ids, *jobtypes, interval=1):
    while True:
        for jt in jobtypes:
            jobs = api.job_take(jt, team_ids)
            for j in jobs:
                yield j
            time.sleep(interval)


def receive_patch(api: WorkerApi, patch_id) -> bytes:
    with TemporaryFile() as f:
        api.patch_get_file(patch_id, f)
        f.seek(0)
        return f.read()


def handle_check_patch(api: WorkerApi, job):
    jobobj = json.loads(job["jobpayload"])
    patch = receive_patch(api, jobobj["patch"])
    success = True
    try:
        patch.decode()
    except UnicodeDecodeError:
        success = False
    if success:
        api.job_result(job["id"], "Success", json.dumps({"feedback": "", "msg": ""}))
    else:
        api.job_result(
            job["id"], "Failed", json.dumps({"feedback": "Invalid UTF-8", "msg": ""})
        )


def handle_patch(api: WorkerApi, job):
    jobobj = json.loads(job["jobpayload"])
    patch = receive_patch(api, jobobj["patch"]).decode()
    team_id = job["team_id"]

    try:
        with app.app_context():
            team = Team.query.filter_by(id=team_id).first()
            team.checker = patch
            db.session.commit()
        logging.info("Team %d's checker has been updated.", team_id)
    except Exception as e:
        logging.error("Update team %d's checker failed: %s", team_id, e)
        api.job_result(job["id"], "Failed", e)
        return
    api.job_result(job["id"], "Success")


with connect_worker_api("patch") as api:
    team_ids = [t["id"] for t in api.teams_get()]
    for job in poll_jobs(api, team_ids, "CheckPatch", "Patch"):
        logging.info("Received job: %s %s", job["id"], job["jobtype"])
        logging.debug("Job: %s", job)
        try:
            if job["jobtype"] == "CheckPatch":
                handle_check_patch(api, job)
            elif job["jobtype"] == "Patch":
                handle_patch(api, job)
        except Exception as e:
            logging.warning("Failed to handle patch update. %s", e)
            import traceback

            traceback.print_exc()

from .models import db, Team
from .app import app
from .worker.api import connect_worker_api, WorkerApi
import json
import time
import logging

logging.root.setLevel(logging.INFO)


def poll_jobs(api: WorkerApi, jobtype, interval=1):
    while True:
        jobs = api.job_take(jobtype, team_ids)
        for j in jobs:
            yield j
        time.sleep(interval)


def handle_flag_update(api: WorkerApi, job):
    team_id = job["team_id"]
    jobobj = json.loads(job["jobpayload"])
    flag = jobobj["flag"]
    try:
        with app.app_context():
            team = Team.query.filter_by(id=team_id).first()
            team.flag = flag
            db.session.commit()
        logging.info("Team %d's flag has been updated to %s.", team_id, flag)
    except Exception as e:
        logging.error("Update team %d's flag failed: %s", team_id, e)
        api.job_result(job["id"], "Failed", e)
        return
    api.job_result(job["id"], "Success")


with connect_worker_api("flag") as api:
    team_ids = [t["id"] for t in api.teams_get()]
    for job in poll_jobs(api, "FlagUpdate"):
        logging.info("Received job: %s", job["id"])
        logging.debug("Job: %s", job)
        try:
            handle_flag_update(api, job)
        except Exception as e:
            logging.warning("Failed to handle flag update. %s", e)

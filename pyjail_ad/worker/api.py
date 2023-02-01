import requests
from urllib.parse import urljoin
import logging
import datetime


API_SERVER = "http://localhost:8088"
API_TOKEN = "0635491c2d34484b992af4450797eebf"
CHALLENGE_ID = 2


class Api:
    def __init__(self, api_server, api_token):
        self.api_server = api_server
        self.api_token = api_token
        logging.info("Api initialized.")

    def request(self, method, path, **kwargs):
        url = urljoin(self.api_server, path)
        if "headers" not in kwargs:
            kwargs["headers"] = {}
        kwargs["headers"]["Authorization"] = self.api_token
        res = requests.request(method, url, **kwargs)
        try:
            resobj = res.json()
        except:
            resobj = {}
        if res.status_code != 200:
            logging.warning(
                "%s %s doesn't get code 200. Code: %d, Response: %s",
                method,
                path,
                res.status_code,
                res.text,
            )
        return res.status_code, resobj

    def teams_get(self):
        rescode, resobj = self.request("GET", "/team")
        return resobj


class WorkerApi:
    def __init__(self, api_server, api_token, worker_name):
        self.api_server = api_server
        self.api_token = api_token
        self.worker_name = worker_name
        self.worker_token = None
        try:
            with open(f"{self.worker_name}.token") as f:
                self.worker_token = f.read()
        except:
            if not self.worker_register():
                return None
        logging.info(
            "Worker initialized. Name: %s Token: %s",
            self.worker_name,
            self.worker_token,
        )

    def request(self, method, path, **kwargs):
        url = urljoin(self.api_server, path)
        if "headers" not in kwargs:
            kwargs["headers"] = {}
        kwargs["headers"]["Authorization"] = self.api_token
        res = requests.request(method, url, **kwargs)
        try:
            resobj = res.json()
        except:
            resobj = {}
        if res.status_code != 200:
            logging.warning(
                "%s %s doesn't get code 200. Code: %d, Response: %s",
                method,
                path,
                res.status_code,
                res.text,
            )
        return res.status_code, resobj

    def worker_register(self):
        rescode, resobj = self.request(
            "POST", "/worker/register", data={"name": self.worker_name}
        )
        if rescode == 200:
            self.worker_token = resobj["token"]
            logging.info(
                "Worker register successful. Name: %s Token: %s",
                self.worker_name,
                self.worker_token,
            )
            try:
                with open(f"{self.worker_name}.token", "w") as f:
                    f.write(self.worker_token)
            except:
                logging.warning(
                    "Couldn't save worker's token into file \"%s\". Please save it into the file manually.",
                    f"{self.worker_name}.token",
                )
            return True
        else:
            logging.error("Worker register failed.")
            return False

    def worker_deregister(self):
        rescode, resobj = self.request("DELETE", f"/worker/{self.worker_token}")
        logging.info("Worker deregistered.")

    def teams_get(self):
        rescode, resobj = self.request("GET", "/team")
        return resobj

    def job_take(self, jobtype, team_ids, challenge_ids=[CHALLENGE_ID], limit=10):
        reqdata = {
            "jobtype": jobtype,
            "team_ids": team_ids,
            "challenge_ids": challenge_ids,
            "worker_token": self.worker_token,
            "limit": limit,
        }
        rescode, resobj = self.request("POST", "/job/take", data=reqdata)
        if rescode == 200:
            return resobj
        else:
            # logging.warning("Call api /job/take failed. StatusCode: %d, Response: %s", rescode, resobj)
            return {}

    def job_result(self, jobid, status, detail="", runat=None):
        if runat is None:
            runat = datetime.datetime.now(datetime.timezone.utc).isoformat()
        reqdata = {
            "status": status,
            "worker_token": self.worker_token,
            "detail": detail,
            "runat": runat,
        }
        rescode, resobj = self.request("POST", f"/job/{jobid}/result", data=reqdata)
        # print(rescode)
        if rescode == 200:
            return True
        return False

    def patch_get_file(self, patchid, dstfile, **kwargs):
        url = urljoin(self.api_server, f"/patch/{patchid}/file")
        if "headers" not in kwargs:
            kwargs["headers"] = {}
        kwargs["headers"]["Authorization"] = self.api_token
        try:
            with requests.request("GET", url, stream=True, **kwargs) as r:
                r.raise_for_status()
                for chunk in r.iter_content(chunk_size=8192):
                    dstfile.write(chunk)
            return True
        except Exception as e:
            logging.warning("Download patch %d's file failed. %s", patchid, e)
        return False

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.worker_deregister()


def connect_api() -> Api:
    return Api(API_SERVER, API_TOKEN)


def connect_worker_api(name) -> WorkerApi:
    worker_name = f"pyjail_ad_{name}"
    api = WorkerApi(API_SERVER, API_TOKEN, worker_name)
    if api is None:
        raise Exception("Couldn't initialize api.")
    return api

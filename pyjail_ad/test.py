import logging

logging.basicConfig()
logger = logging.getLogger("patch_worker")
logger.setLevel(logging.INFO)

# from .models import db, Team
# from .app import app
# from .worker.api import connect_worker_api, WorkerApi
from tempfile import TemporaryFile
from . import sandbox
from pathlib import Path
from multiprocessing import Pool
import json
import time

# import signal
# import os

# def handle_interrupt(*args, **kwargs):
#     exit()


# signal.signal(signal.SIGINT, handle_interrupt)
# signal.signal(signal.SIGTERM, handle_interrupt)


PATCH_CHECK = []
for f in (Path(__file__).parent / "patch_check").iterdir():
    code = f.read_text()
    r = sandbox.run(code)
    PATCH_CHECK.append((f.name, code, r.exit_code, r.stdout, r.stderr))


def test(p):
    feedback = ""
    try:
        for name, code, exit_code, stdout, stderr in PATCH_CHECK:
            allow, new_code = sandbox.apply_jail(p, code)
            print(name, allow, new_code)
            if not allow:
                feedback = f"Your jail wrongly rejected the patch checking code.\nFilename: {name}"
                break
            r = sandbox.run(new_code)
            if r.exit_code != exit_code or r.stdout != stdout or r.stderr != stderr:
                feedback = f"Your jail changed the output of patch checking code.\nFilename: {name}"
                break
    except UnicodeDecodeError:
        feedback = "Yout patch is not a valid UTF-8 string."
    print(feedback)


def test2(p):
    feedback = ""
    try:
        res = sandbox.apply_jail_batch(p, [code for _, code, _, _, _ in PATCH_CHECK])

        for (name, code, exit_code, stdout, stderr), (allow, new_code) in zip(
            PATCH_CHECK, res
        ):
            # allow, new_code = sandbox.apply_jail(p, code)
            print(name, allow)
            if code != new_code:
                # print(code)
                print(new_code)
            if not allow:
                feedback = f"Your jail wrongly rejected the patch checking code.\nFilename: {name}"
                break
            r = sandbox.run(new_code)
            if r.exit_code != exit_code or r.stdout != stdout:
                feedback = f"Your jail changed the output of patch checking code.\nFilename: {name}"
                print(r.stdout)
                print(stdout)
                print(r.stderr)
                print(stderr)
                break
    except UnicodeDecodeError:
        feedback = "Yout patch is not a valid UTF-8 string."
    print(feedback)


j = r'''
from typing import Tuple

def jail(code: str) -> Tuple[bool, str]:
    code = '_as98829342_ = 10\n' + code
    #exec=open=os.popen=os.system=os.exec=os.read=0\n" + code

    return True, code
'''
test2(j)
c = r'''

'''
a, nc = sandbox.apply_jail(j, c)
print(a)
r = sandbox.run(nc, files=[{
    "name": "flag.txt",
    "content": "flag{test}".encode()
}])
# r = sandbox.run(
#     """
# import os
# os.system('id')
# os.system('ls -l')
# os.system('rm flag.txt')
# print(open('flag.txt').read())
# open("flag.txt", "w").write('123')
# os.system('ls -l')
# print(123)
# print(open('flag.txt').read())
# """,
#     files=[
#         {
#             "name": "flag.txt",
#             "content": b"test_flag",
#         }
#     ],
# )
print(r.stdout.decode())
print(r.stderr.decode())

from subprocess import run, PIPE, DEVNULL

DB = "/tmp/hashcash.db"
BITS = 24


def mint(resource):
    return (
        run(["hashcash", f"-mb{BITS}", resource], stdout=PIPE, stderr=DEVNULL)
        .stdout.decode()
        .strip()
    )


def mint_cmd(resource):
    return " ".join(["hashcash", f"-mb{BITS}", resource])


def check(resource, stamp):
    r = run(
        ["hashcash", f"-cdb{BITS}", "-r", resource, stamp, "-f", DB],
        stdout=DEVNULL,
        stderr=DEVNULL,
    )
    return r.returncode == 0

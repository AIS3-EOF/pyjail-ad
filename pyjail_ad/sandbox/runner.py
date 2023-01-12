import epicbox
from dataclasses import dataclass


epicbox.configure(profiles=[epicbox.Profile("python", "python:3.10-alpine")])


@dataclass
class Result:
    exit_code: int
    stdout: bytes
    stderr: bytes
    duration: float
    timeout: bool
    oom_killed: bool


DEFAULT_LIMITS = {"cputime": 1, "memory": 64}


def run(code: str, files=[], limits=DEFAULT_LIMITS, **kwargs) -> Result:
    files = [{"name": "main.py", "content": code.encode()}] + files
    result = epicbox.run(
        "python", "python3 main.py", files=files, limits=limits, **kwargs
    )
    return Result(**result)

from .runner import run

CHECKER_TEMPLATE = """{}

import sys
print(check(sys.stdin.read()))
"""

DEFAULT_CHECKER = """def check(s):
    return True
"""


def check(checker: str, code: str) -> bool:
    r = run(CHECKER_TEMPLATE.format(checker), stdin=code)
    return r.stdout.strip() != b"False"  # allow by default

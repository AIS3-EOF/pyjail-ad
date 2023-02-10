from .runner import run
import json

JAIL_TEMPLATE = """{}

import sys, json
print(json.dumps(jail(sys.stdin.read())))
"""

MAX_MORE_CODE = 75

DEFAULT_JAIL = f"""from typing import Tuple

def jail(code: str) -> Tuple[bool, str]:
    '''
    This function should return a tuple of two values:
    - first value is a boolean indicating whether the code should be run or not
    - second value is the modified the code, but it must satisfy len(new_code) <= len(code) + {MAX_MORE_CODE} or your jail will be ignored

    You also shouldn't print anything to stdout here.
    '''
    return True, code
"""


def apply_jail(jail: str, code: str) -> bool:
    try:
        r = run(JAIL_TEMPLATE.format(jail), stdin=code)
        allow, new_code = json.loads(r.stdout.strip())
        if len(new_code) > len(code) + MAX_MORE_CODE:
            return True, code
        return allow, new_code
    except:
        # allow by default
        return True, code

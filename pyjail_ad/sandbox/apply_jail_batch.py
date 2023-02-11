from .apply_jail import MAX_MORE_CODE
from .runner import run
import json

JAIL_TEMPLATE = """{}

import sys, json
codes = json.loads(sys.stdin.read())
res = []
for code in codes:
    res.append(jail(code))
print(json.dumps(res))
"""

def apply_jail_batch(jail: str, codes: str) -> bool:
    stdin = json.dumps(codes)
    try:
        r = run(JAIL_TEMPLATE.format(jail), stdin=stdin)
        results = json.loads(r.stdout.strip())
        ret = []
        for code, (allow, new_code) in zip(codes, results):
            if len(new_code) > len(code) + MAX_MORE_CODE:
                ret.append((True, code))
            else:
                ret.append((allow, new_code))
        return ret
    except Exception as e:
        # allow by default
        return [(True, code) for code in codes]

"""OSTF 2.3 standalone candidate CLI. No device dependency.
Usage: python ostf23_validate.py [--json] FILE [FILE ...]
Returns 0 only when every file is conformant, 1 when any file fails, 2 on usage error.
"""
import argparse
import json
from pathlib import Path
from strict_json109 import check_wire

def validate_paths(paths):
    outcomes=[]
    for path in paths:
        try:
            issues=check_wire(Path(path).read_bytes())
        except OSError as exc:
            issues=[f"file IO error: {exc.strerror or str(exc)}"]
        outcomes.append({"file":str(path),"valid":not issues,"errors":issues})
    return outcomes

def main(argv=None):
    p=argparse.ArgumentParser(description='Validate standalone OSTF 2.3 candidate files')
    p.add_argument('--json',action='store_true',help='machine-readable JSON output')
    p.add_argument('files',nargs='+')
    args=p.parse_args(argv)
    outcomes=validate_paths(args.files)
    if args.json:
        print(json.dumps({"profile":"OSTF-2.3-standalone-candidate113","results":outcomes},ensure_ascii=False,indent=2))
    else:
        for item in outcomes:
            print(('PASS' if item['valid'] else 'FAIL')+' '+item['file'])
            for error in item['errors']:
                print('  - '+error)
    return 0 if all(item['valid'] for item in outcomes) else 1

if __name__=='__main__':
    raise SystemExit(main())

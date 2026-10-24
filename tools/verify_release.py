from pathlib import Path
import sys, subprocess, hashlib, json
root=Path(__file__).resolve().parents[1]
samples=sorted((root/'samples').glob('*.ostf'))
assert samples, 'no samples'
p=subprocess.run([sys.executable,str(root/'ostf23_validate.py'),'--json',*(str(s) for s in samples)],cwd=root,capture_output=True,text=True)
if p.returncode:
 print(p.stdout);print(p.stderr);raise SystemExit(p.returncode)
report=json.loads(p.stdout);assert len(report['results'])==len(samples) and all(x['valid'] for x in report['results'])
files=[p for p in root.rglob('*') if p.is_file() and not ('__pycache__' in p.parts)]
print(f'PASS {len(samples)} OSTF samples; {len(files)} repository files (limit 100)')
assert len(files)<=100

#!/usr/bin/env python3
"""Build all sources and record real MPI test output. Run inside Ubuntu WSL."""
import json
import math
import pathlib
import re
import shutil
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
RESULTS = ROOT / 'results'
RESULTS.mkdir(exist_ok=True)
records = []

def execute(name, command, verify=lambda p: p.returncode == 0):
    try:
        p = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, timeout=130)
        validation_error = None
        try:
            passed = verify(p)
        except (ValueError, KeyError, StopIteration, OverflowError) as exc:
            passed = False
            validation_error = f'{type(exc).__name__}: {exc}'
        item = dict(name=name, command=command, status='PASS' if passed else 'FAIL',
                    exit_code=p.returncode, stdout=p.stdout, stderr=p.stderr)
        if validation_error:
            item['validation_error'] = validation_error
    except subprocess.TimeoutExpired as exc:
        def decode(value):
            return value.decode(errors='replace') if isinstance(value, bytes) else value or ''
        item = dict(name=name, command=command, status='FAIL', error=str(exc),
                    stdout=decode(exc.stdout), stderr=decode(exc.stderr))
    except OSError as exc:
        item = dict(name=name, command=command, status='NOT TESTED', error=str(exc))
    records.append(item)
    (RESULTS / 'test_results.json').write_text(json.dumps(records, indent=2))
    print(name, item['status'], flush=True)
    return item['status'] == 'PASS'

def mpi(name, n, check=None, seconds=30, expected=0):
    def verify(p):
        return p.returncode == expected and (check is None or check(p.stdout))
    return execute(f'{name} ({n} ranks)',
                   ['timeout', '--kill-after=2s', f'{seconds}s', 'mpirun', '-n', str(n),
                    str(ROOT / 'build' / name)], verify)

def data(out):
    line = next(line for line in out.splitlines() if line.startswith('exercise='))
    return dict(field.split('=', 1) for field in line.split(','))

def pi_ok(out):
    d = data(out)
    return int(d['samples']) == 10000000 and 0 <= int(d['inside']) <= 10000000 and abs(float(d['result']) - math.pi) < 0.005 and abs(
        float(d['result']) - 4 * int(d['inside']) / 10000000) < 1e-10

def messages(out, ordered=False):
    found = [(int(v), int(r)) for v, r in re.findall(r'Received (\d+) from rank (\d+)', out)]
    expected = [(100, 1), (200, 2), (300, 3)]
    return (found if ordered else sorted(found)) == expected

def main():
    missing = [x for x in ('mpicxx', 'mpirun', 'timeout') if not shutil.which(x)]
    if missing:
        for tool in missing:
            execute('Missing prerequisite: ' + tool, [tool, '--version'])
        print('BLOCKED: missing ' + ', '.join(missing))
        return 2
    (ROOT / 'build').mkdir(exist_ok=True)
    built = []
    for source in sorted((ROOT / 'src').rglob('*')):
        if source.suffix not in ('.c', '.cc', '.cpp'):
            continue
        built.append(execute('Compile ' + str(source.relative_to(ROOT)),
            ['mpicxx', '-x', 'c++', '-std=c++17', '-O2', '-Wall', '-Wextra',
             str(source), '-o', str(ROOT / 'build' / source.stem)]))
    if not all(built):
        return 1
    for n in (1, 4):
        mpi('ex0_hello', n, lambda out, n=n: sorted(int(r) for r in
            re.findall(r'Hello from rank (\d+) of '+str(n), out)) == list(range(n)))
        mpi('HelloMPI', n, lambda out, n=n: sorted(int(r) for r in
            re.findall(r'From rank (\d+)', out)) == list(range(n)))
    mpi('messages1', 4, lambda out: 'the value of y is 30' in out)
    array = ' '.join(str(i * 10) for i in range(10))
    mpi('messaage2', 4, lambda out: array in ' '.join(out.split()))
    for n in (1, 2, 3, 4, 8):
        mpi('ex2_sum', n, lambda out: data(out)['result'] == '50000005000000')
        mpi('ex3_pi', n, pi_ok, seconds=120)
    mpi('ex5_bsend', 2, lambda out: all(prefix + array in ' '.join(out.split())
        for prefix in ('Sender original x: ', 'Receiver y: ')))
    mpi('ex5_faculty_bsend', 4, lambda out: all(prefix + array in ' '.join(out.split())
        for prefix in ('Rank 1 retained x: ', 'Rank 3 received y: ')))
    mpi('ex5_mismatch', 3, lambda out: 'rank 1 waiting for rank 2' in out,
        seconds=5, expected=124)
    mpi('ex6_specific_source', 4, lambda out: messages(out, ordered=True))
    mpi('ex6_any_source', 4, messages)
    mpi('ex7_any_source_bsend', 4, lambda out: messages(out) and
        all(f'Rank {r} retained original value {r*100}' in out for r in (1, 2, 3)))
    for name, n in (('ex5_mismatch', 2), ('ex5_bsend', 1),
                    ('ex5_faculty_bsend', 3), ('ex6_specific_source', 1),
                    ('ex6_any_source', 1), ('ex7_any_source_bsend', 1)):
        mpi(name, n, lambda out: True, expected=1)
    return 0 if all(r['status'] == 'PASS' for r in records) else 1

if __name__ == '__main__':
    sys.exit(main())

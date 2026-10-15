#!/usr/bin/env python3
"""Record prerequisite checks and attempt to compile every project source."""
import ast
import json
import pathlib
import shutil
import subprocess
import sys

root = pathlib.Path(__file__).resolve().parent.parent
lines = []
failed = False
for config in sorted((root / '.vscode').glob('*.json')):
    json.loads(config.read_text(encoding='utf-8-sig'))
    lines.append(f'VS Code JSON syntax PASS: {config.name}')
for name in ('mpicxx', 'mpicc', 'mpirun', 'g++', 'gcc', 'python3', 'timeout'):
    lines.append(f'{name}: {shutil.which(name) or "NOT FOUND"}')
    if name in ('mpicxx', 'mpirun', 'g++', 'python3', 'timeout') and not shutil.which(name):
        failed = True
try:
    import matplotlib
    lines.append(f'matplotlib: {matplotlib.__version__}')
except ImportError as exc:
    lines.append(f'matplotlib: {exc}')
    failed = True
for source in sorted((root / 'scripts').glob('*.py')):
    ast.parse(source.read_text())
    lines.append(f'Python syntax PASS: {source.name}')
lines.append(f'Arithmetic reference only (not MPI): {10000000 * 10000001 // 2}')
for source in sorted((root / 'src').rglob('*')):
    if source.suffix not in ('.c', '.cc', '.cpp'):
        continue
    # Faculty HelloMPI.c contains C++ headers despite its .c suffix.
    compiler = 'mpicxx'
    command = [compiler, '-x', 'c++', '-std=c++17', '-O2', '-Wall', '-Wextra', str(source), '-o', str(root / 'build' / source.stem)]
    if shutil.which(compiler):
        (root / 'build').mkdir(exist_ok=True)
    try:
        result = subprocess.run(command, text=True, capture_output=True, timeout=60)
        lines.append(f'Compile {source.name}: exit {result.returncode}\n{result.stdout}{result.stderr}')
        failed = failed or result.returncode != 0
    except (OSError, subprocess.TimeoutExpired) as exc:
        lines.append(f'Compile BLOCKED {source.name}: {exc}')
        failed = True
output = '\n'.join(lines) + '\n'
(root / 'results').mkdir(exist_ok=True)
(root / 'results' / 'environment_check.txt').write_text(output)
print(output, end='')
sys.exit(1 if failed else 0)

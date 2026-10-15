#!/usr/bin/env python3
"""Configure VS Code using the actual Ubuntu Open MPI installation."""
import json
import pathlib
import shlex
import shutil
import subprocess
import sys

def main():
    if sys.platform != 'linux':
        sys.exit('Run this script inside Ubuntu WSL, with the folder open in VS Code WSL mode.')
    compiler = shutil.which('mpicxx')
    if not compiler:
        sys.exit('mpicxx missing: sudo apt install openmpi-bin libopenmpi-dev g++')
    probe = subprocess.run([compiler, '-x', 'c++', '-std=c++17', '-fsyntax-only', '-'],
        input='#include <mpi.h>\n#include <iostream>\n#include <algorithm>\n#include <cstdlib>\nint main() {}\n',
        text=True, capture_output=True)
    if probe.returncode:
        sys.exit(probe.stdout + probe.stderr)
    result = subprocess.run([compiler, '--showme:incdirs'], check=True,
                            text=True, capture_output=True)
    includes = shlex.split(result.stdout)
    root = pathlib.Path(__file__).resolve().parent.parent
    config = {'configurations': [{
        'name': 'Linux', 'compilerPath': compiler, 'compilerArgs': ['-x', 'c++'],
        'includePath': ['${workspaceFolder}/src/**', *includes],
        'cStandard': 'c17', 'cppStandard': 'c++17', 'intelliSenseMode': 'linux-gcc-x64'
    }], 'version': 4}
    target = root / '.vscode' / 'c_cpp_properties.json'
    target.parent.mkdir(exist_ok=True)
    target.write_text(json.dumps(config, indent=2) + '\n')
    print('Header probe PASS. Configured', target, 'with', compiler, 'and', includes)

if __name__ == '__main__':
    main()

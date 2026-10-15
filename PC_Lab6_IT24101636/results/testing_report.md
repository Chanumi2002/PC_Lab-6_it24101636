# SE4060 MPI Lab 6 testing report

Date: 2026-10-15 (Asia/Colombo).

## Actual outcome

### IntelliSense correction pass

Inspected all 12 C/C++ sources and the live VS Code Problems panel. The panel
showed four diagnostics in ex5_faculty_bsend.cpp: include errors detected,
missing mpi.h, missing iostream, and missing vector. The editor was a local
Windows window using windows-gcc-x64 with compilerPath gcc, not Ubuntu WSL.
The reported standard/MPI header errors are dependency/configuration errors;
no source syntax error is established by those messages.

Changed c_cpp_properties.json to Linux C++17, /usr/bin/mpicxx, and conventional
Ubuntu x86-64 MPI include paths. These paths are installation targets, not currently
verified files: Ubuntu still lacks /usr/lib/x86_64-linux-gnu/openmpi/include/mpi.h
and /usr/include/c++. Added configure_intellisense.py to compile a real header
probe and use installed mpicxx --showme:incdirs output before claiming header
availability. It currently exits with the accurate missing-mpicxx message.
Removed conflicting Windows-specific runner settings, associated faculty
HelloMPI.c with C++, added WSL tasks/extension recommendations, and corrected
the old hardcoded nonexistent debug executable path. Debugging is optional and
requires gdb. No required source includes were removed or errors suppressed.

Reran all 12 compilation attempts; each remains blocked by missing mpicxx.
All five Python scripts pass syntax parsing. The test runner reports missing
prerequisites as NOT TESTED; there are no actual MPI outputs to verify.
Sudo still reports interactive authentication required. The editor cannot be
certified free of Problems until dependencies exist and it runs in WSL mode.

Installed Microsoft's WSL extension v0.104.3 successfully. Opened the project
in a new window and verified the title `SE4060_MPI_Lab6 [WSL: Ubuntu] - Visual
Studio Code`. All five .vscode JSON files pass JSON parsing. The final
environment check exits 1 as expected for missing prerequisites; all twelve
compile attempts remain blocked. See environment_check.txt for the latest log.

Latest correction pass supersedes earlier tooling descriptions: missing
prerequisites or failed builds now make the environment checker return exit 1.
Invalid program output records FAIL instead of crashing the suite. Elapsed test
timeouts record FAIL with captured output; each missing tool is checked
individually. Pi now reports its sample count for validation, and sum timing
prints 12 significant digits. Benchmarks reject nonfinite timeout/Pi values,
check prerequisites, use GNU timeout with a kill deadline, and save each
validated measurement immediately. These corrections do not constitute
successful MPI execution. Installation was retried and still requires
interactive sudo authentication.

The lab is NOT completed. Dependency installation was attempted using
`wsl -d Ubuntu -- sudo -n apt update`; Ubuntu returned exit 1:
`sudo: interactive authentication is required`.
The user must authenticate in their own terminal. Installation has not succeeded
and no MPI execution, timing measurement, Pi estimate, or graph is claimed.
No Git initialization, commit, push, or remote modification was performed.

## Environment and compilation

The accessible WSL distribution is Ubuntu 26.04 LTS, WSL 2, user mahaw (UID 1000).
The system reports 12 logical processors. Ubuntu and docker-desktop are the only
listed WSL distributions. Windows PATH also lacked MPI and GCC/G++ in prior checks.
The latest Ubuntu check still found no mpicxx, mpicc, mpirun, g++, or gcc.
Python 3 and timeout are available; matplotlib import fails.

All 12 current C/C++ sources were submitted to compile attempts. Every attempt
failed before compilation with `[Errno 2] No such file or directory: 'mpicxx'`.
There are no compiler diagnostics verifying or disproving source correctness.
See [environment_check.txt](environment_check.txt) for each source's outcome.
The intended build uses mpicxx, C++17, -O2, -Wall, -Wextra. Faculty HelloMPI.c uses
C++ headers despite its extension, so the build explicitly uses `-x c++`.

All four Python scripts pass AST syntax parsing under Ubuntu Python.
The automated suite was invoked and correctly stopped at missing prerequisites;
[test_results.json](test_results.json) records NOT TESTED rather than PASS.

## Exercise summary

| Exercise | Status | Actual evidence and remaining work |
|---|---|---|
| 0 | NOT TESTED | Three original faculty sources downloaded and preserved; modernized Hello retained. Builds and executions blocked. |
| 1 | PASS for local preparation; submission deferred | Source, script, result and ignore structure prepared. No commit/push authorized or performed. Student-ID repository creation/submission remains outstanding. |
| 2 | NOT TESTED | Independent Python arithmetic confirms 50000005000000, but MPI sum has not executed. Tests cover 1, 2, 3, 4, 8 ranks once tools exist. |
| 3 | NOT TESTED | Source distributes exactly 10,000,000 samples using deterministic per-rank seeds. No samples executed; no observed Pi estimate. |
| 4 | NOT TESTED | Benchmark now calculates means and medians from five runs at 1, 2, 4, 8 ranks; speedup uses mean T1/Tp. No measurements or PNGs exist. |
| 5 | NOT TESTED | Intentional mismatch, two-rank Bsend, and faculty array Bsend adaptation prepared. No communication execution. |
| 6 | NOT TESTED | Fixed-source and ANY_SOURCE tests prepared; no observed message order. |
| 7 | NOT TESTED | Bsend buffer sizing and message checks prepared; no observed transfer. |

Expected results below are criteria, not observations. No skipped test is passed.

## Sources and implementation review

Preserved originals under src/faculty were downloaded from the public faculty
repository linked in the README. They remain unmodified; see PROVENANCE.md.
messages1.cc sends the integer 30 from rank 1 to rank 3 with MPI_Ssend.
messaage2.cc sends ten integers 0, 10, ..., 90 between those ranks.
ex5_faculty_bsend.cpp adapts the latter with MPI_Bsend, MPI_Pack_size,
MPI_BSEND_OVERHEAD, attached storage retained until detach, and unchanged x.
The additional ex5_bsend.cpp uses ranks 0 and 1.

Previous review fixes retained: ex5_mismatch rejects fewer than three ranks;
ex2_sum returns a failure exit code if rank 0 sees an incorrect total.
Benchmark arguments, reported process count, sum, Pi tolerance, and positive finite
timing values are checked. Every individual benchmark output and measurement will
be saved to benchmark_raw.csv after successful benchmarking. No C++ change is
runtime-validated yet.

## Test plan implemented in scripts/test_lab.py

- Compile every .c/.cc/.cpp recursively, preserving build output and exit codes.
- Hello at 1 and 4 ranks: each rank appears exactly once.
- Original faculty scalar and array transfers at 4 ranks.
- Sum at 1, 2, 3, 4, 8 ranks: exactly 50000005000000; 3 ranks tests uneven work.
- Pi at the same counts: error below 0.005, approximately six sampling standard
  errors at 10 million samples, and agreement with 4*inside/10000000.
- Both buffered-array examples: correct values and retained sender originals.
- Intentional mismatch: timeout after 5 seconds with expected exit 124 and the
  waiting-receiver diagnostic. GNU timeout has a further 2-second kill limit.
  A different termination code is recorded as failure for investigation.
- Fixed-source receive order 1, 2, 3 versus unconstrained ANY_SOURCE order,
  checking each corresponding value 100, 200, 300 exactly once.
- ANY_SOURCE Bsend: same values and sender retention messages.
- Invalid process counts: expected exit 1 for messaging guards.

All MPI tests have launch time limits. Raw commands, stdout, stderr and exit codes
are retained in test_results.json. The benchmark has a 120-second launcher timeout
per run; intentional deadlocks use GNU timeout rather than that Python timeout.

## Ambiguities and limitations

1. The full original lab sheet is absent. The faculty README labels Hello as
   Exercise 1 while this project calls it Exercise 0 and reserves 1 for GitHub.
2. The local README reports that Exercise 6 refers to Exercise 3 while requesting
   MPI_ANY_SOURCE. The Pi solution has reductions, not receives. This project uses
   a separate worker-messaging demonstration, reused with Bsend for Exercise 7.
   Exact compliance must be checked against the original lab sheet.
3. Faculty originals use char name[30] for processor names, which is smaller than
   MPI_MAX_PROCESSOR_NAME and can overflow for a long hostname. Originals remain
   preserved; modernized Hello uses the MPI constant.
4. MPI_ANY_SOURCE allows any matching sender and can still produce rank order.
   MPI_Bsend permits reuse of the original send buffer when it returns; the code
   conservatively keeps it unchanged until detach. Detach can block until pending
   buffered messages complete.
5. MPI_Wtime timing excludes launcher startup and includes computation plus the
   first result reduction. The later reduction collecting maximum rank elapsed
   time is outside the measured interval. Machine load and scheduling can dominate
   the short sum task; a speedup is not guaranteed.
6. Pi seeds depend on process rank; the workload size is fixed but sampled points
   change with process count. PRNG streams have distinct seeds, without a formal
   proof of statistical independence. Five repeated runs with the same count reuse
   the same deterministic stream on the same implementation.
7. Graph output was changed to results/graphs/ and speedup now uses averages,
   matching the latest user request. Earlier instructions using median speedups
   and a top-level graphs directory have been superseded.

## Unblock and reproduce

In an interactive terminal run:

```powershell
wsl -d Ubuntu
```

Then run inside Ubuntu and enter the sudo password there:

```bash
sudo apt update && sudo apt install -y openmpi-bin libopenmpi-dev g++ python3-matplotlib
cd /mnt/c/Users/mahaw/Downloads/SE4060_MPI_Lab6/SE4060_MPI_Lab6
mpicxx --version
mpirun --version
g++ --version
python3 scripts/check_environment.py
python3 scripts/test_lab.py
# Continue only if the correctness suite passes:
python3 scripts/benchmark.py --counts 1 2 4 8 --repeat 5
MPLBACKEND=Agg python3 scripts/plot.py
```

Expected deliverables after successful runs: benchmark.csv, benchmark_raw.csv,
test_results.json, and four PNGs in results/graphs/. These are not yet available
as successful test evidence. Update this report with observed outputs and measured
times after execution. GitHub submission still requires user approval.

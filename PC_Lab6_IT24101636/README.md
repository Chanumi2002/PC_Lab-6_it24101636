# SE4060 Lab Sheet 6: MPI

Standalone educational solutions for Exercises 0-7, based on the faculty starter repository: https://github.com/SLIIT-FacultyOfComputing/SE4060-MPI-Part1 .

## Requirements

- Linux, Ubuntu/WSL or HPC node with an MPI implementation (Open MPI or MPICH), C++ compiler, Python 3, matplotlib.
- Ubuntu example: `sudo apt update && sudo apt install -y openmpi-bin libopenmpi-dev g++ python3-matplotlib`
- Check `mpicxx --version` and `mpirun --version`.

## Build and run

### VS Code and missing headers

Open this folder in **WSL: Ubuntu**, not a local Windows editor window. Use the
Command Palette command **WSL: Reopen Folder in WSL** (Microsoft's WSL extension
is required), then install the Microsoft C/C++ extension in WSL when prompted.
Linux `/usr/...` paths cannot be used by a C/C++ extension running on Windows.

Inside Ubuntu, install dependencies and configure the editor from the real tools:

```bash
sudo apt update && sudo apt install -y openmpi-bin libopenmpi-dev g++ python3-matplotlib
python3 scripts/configure_intellisense.py
python3 scripts/test_lab.py
```

The checked-in `.vscode/c_cpp_properties.json` targets Ubuntu x86-64 using
`/usr/bin/mpicxx` and Ubuntu's usual Open MPI include directories. Those paths
require installation first. The setup script compiles a header probe and replaces
the MPI include paths with `mpicxx --showme:incdirs` output. The compiler supplies
its own version-specific C++ standard-library paths; no guessed GCC version is
hardcoded. `HelloMPI.c` is associated with C++ because the faculty file uses C++
headers. Error diagnostics remain enabled. The WSL build/test task is available
through Ctrl+Shift+B. Optional one-rank debugging requires `sudo apt install gdb`;
use `mpirun` for the multi-rank exercises.

If header errors persist after installation and reopening in WSL, run **C/C++:
Reset IntelliSense Database**, then reload the window. This refreshes indexing;
it does not replace installing the compiler and MPI development headers.

```bash
mkdir -p build
python3 scripts/test_lab.py
mpirun -n 4 ./build/ex0_hello
mpirun -n 4 ./build/ex2_sum
mpirun -n 4 ./build/ex3_pi
mpirun -n 2 ./build/ex5_bsend
mpirun -n 4 ./build/ex6_specific_source
mpirun -n 4 ./build/ex6_any_source
mpirun -n 4 ./build/ex7_any_source_bsend
```

**Intentional hang demonstration:** `timeout 5s mpirun -n 3 ./build/ex5_mismatch`. Rank 1 waits for rank 2, but rank 2 never sends. For some MPI implementations sender may block too. Do not run without timeout. The sender is rank 0, the receiver expects rank 2.

Exercise 0: unmodified faculty `HelloMPI.c`, `messages1.cc`, and `messaage2.cc` are preserved under `src/faculty/`. `scripts/test_lab.py` compiles all sources recursively using `mpicxx -x c++ -std=c++17 -O2 -Wall -Wextra` and runs output/exit-code checks. The `.c` starter contains C++ headers, so it is deliberately compiled as C++. Run `mpirun -n 4 ./build/HelloMPI`, `mpirun -n 4 ./build/messages1`, and `mpirun -n 4 ./build/messaage2` for the original examples. Their processor-name arrays are only 30 bytes; this upstream limitation is preserved. `ex0_hello.cpp` uses `MPI_MAX_PROCESSOR_NAME` instead.

`MPI_Comm_rank` identifies a process within its communicator; `MPI_Comm_size` gives the process count. Send selects a destination and tag; receive selects a source and tag within the same communicator. The faculty programs send from rank 1 to rank 3, so use at least four processes.

Exercise 1: Create a GitHub repository named after your own student ID, commit these source files and result plots there. This archive itself is not uploaded to GitHub.

Exercise 2: partitions the interval 1..10,000,000 over processes; all results are combined using `MPI_Reduce`. Correct answer is `50000005000000` (64-bit integer).

Exercise 3: generates exactly 10,000,000 2D points in the unit square. Counts how many lie inside the quarter unit circle and estimates pi by 4 * inside / N. Each rank has an independent deterministic PRNG seed. Due to sampling randomness, π estimates vary by run configuration.

Exercise 4: collect measurements on **the same machine** with process counts 1, 2, 4, 8. The benchmark records five individual runs per configuration, calculates average and median times, and computes speedup as average T1 / average Tp. Do **not** submit made-up times or speedups.

```bash
python3 scripts/benchmark.py --counts 1 2 4 8 --repeat 5
MPLBACKEND=Agg python3 scripts/plot.py
```

**Timing interpretation:** `MPI_Wtime()` measures time from a pre-computation synchronization barrier to completion of `MPI_Reduce`, reporting the maximum elapsed rank time. Benchmarks include local compute and result reduction, not MPI startup. For a meaningful strong-scaling comparison, keep workload and hardware fixed. Sum of 10 million integers is too small to reliably benefit from many MPI processes on most modern computers; slower parallel runs are expected and scientifically valid.

Exercise 5: shows that receiving from the wrong source causes blocking because source and tag must match. A mismatch in destination/source is not automatically repaired. The buffered-send version uses an attached MPI buffer, leaves the sending array unchanged, and detaches the buffer to ensure completion.

`mpirun -n 4 ./build/ex5_faculty_bsend` is the buffered adaptation of faculty `messaage2.cc`: ten integers are sent from rank 1 to rank 3. `ex5_bsend` supplies an additional two-process variant. The intentional mismatch test uses `timeout --kill-after=2s 5s mpirun -n 3 ./build/ex5_mismatch`; timeout exit 124 is expected. The test runner bounds all MPI launches and records actual output in `results/test_results.json`.

Exercise 6: the sheet references 'Exercise 3' but also `MPI_ANY_SOURCE`; Monte Carlo pi has no `MPI_Recv` to change, so this file uses a multiple-worker messaging demonstration to show the requested receive-source difference. Original receives in rank order, new version receives in arrival order. Numerical data should match; arrival order can vary.

Exercise 7: same any-source messaging demonstration, replacing worker-side `MPI_Send` with `MPI_Bsend` plus a correctly sized attached buffer and safe buffer detach.

## Results

`results/benchmark.csv`, `results/benchmark_raw.csv`, and `results/graphs/*.png` are created only after actual benchmark runs. Raw CSV includes each timing, result, stdout and stderr. `results/testing_report.md` states observed status and remaining limitations. No successful execution is implied by the availability of scripts.

Run from the Ubuntu WSL project directory:

```bash
python3 scripts/check_environment.py
python3 scripts/test_lab.py
python3 scripts/benchmark.py --counts 1 2 4 8 --repeat 5
MPLBACKEND=Agg python3 scripts/plot.py
```

Run the benchmark only after the correctness suite passes. The suite also tests three processes for uneven work distribution and invalid process counts for messaging programs. Pi uses a tolerance of 0.005 around mathematical pi, roughly six sampling standard errors for 10 million samples, and checks the estimate against the reported inside-circle count. The sample count is fixed by the source.

## Git

```bash
git init
git add .
git commit -m "Complete MPI lab 6 exercises"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_STUDENT_ID.git
git push -u origin main
```

Do not push build binaries. Add them to `.gitignore` (included).

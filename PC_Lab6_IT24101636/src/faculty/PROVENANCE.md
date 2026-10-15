# Preserved faculty starter programs

Downloaded without source edits from:
https://github.com/SLIIT-FacultyOfComputing/SE4060-MPI-Part1/tree/main

- HelloMPI.c
- messages1.cc
- messaage2.cc (upstream spelling preserved)

The automated build uses C++ mode even for HelloMPI.c because it includes cstdio
and cstdlib. Messaging requires four ranks (sender 1, receiver 3). Original
processor-name buffers contain 30 bytes; MPI recommends MPI_MAX_PROCESSOR_NAME.
These sources remain unchanged to preserve the originals. The modernized Hello
and buffered-send adaptation are separate files under src/.

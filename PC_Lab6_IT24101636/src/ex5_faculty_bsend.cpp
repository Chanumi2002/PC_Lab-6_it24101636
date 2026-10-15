// Buffered-send adaptation of faculty/messaage2.cc. Original is preserved there.
#include <mpi.h>
#include <iostream>
#include <vector>
int main(int argc, char** argv) {
    MPI_Init(&argc, &argv);
    int rank, size;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);
    if (size < 4) {
        if (rank == 0) std::cerr << "Run with at least 4 processes\n";
        MPI_Finalize();
        return 1;
    }
    int x[10], y[10] = {};
    if (rank == 1) {
        for (int i = 0; i < 10; ++i) x[i] = 10 * i;
        int packed;
        MPI_Pack_size(10, MPI_INT, MPI_COMM_WORLD, &packed);
        std::vector<char> buffer(packed + MPI_BSEND_OVERHEAD);
        MPI_Buffer_attach(buffer.data(), static_cast<int>(buffer.size()));
        MPI_Bsend(x, 10, MPI_INT, 3, 0, MPI_COMM_WORLD);
        void* detached = nullptr;
        int bytes;
        MPI_Buffer_detach(&detached, &bytes);
        std::cout << "Rank 1 retained x:";
        for (int value : x) std::cout << ' ' << value;
        std::cout << '\n';
    } else if (rank == 3) {
        MPI_Recv(y, 10, MPI_INT, 1, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
        std::cout << "Rank 3 received y:";
        for (int value : y) std::cout << ' ' << value;
        std::cout << '\n';
    }
    MPI_Finalize();
    return 0;
}

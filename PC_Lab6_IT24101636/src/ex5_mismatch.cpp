#include <mpi.h>
#include <iostream>
// Deliberately wrong source: rank 0 sends, while rank 1 waits for rank 2.
// Run with a timeout: timeout 5s mpirun -n 3 ./ex5_mismatch
int main(int argc,char** argv){
 MPI_Init(&argc,&argv);int rank,size;MPI_Comm_rank(MPI_COMM_WORLD,&rank);MPI_Comm_size(MPI_COMM_WORLD,&size);
 if(size<3){if(rank==0)std::cerr<<"Run with at least 3 processes\n";MPI_Finalize();return 1;}
 if(rank==0){int value=42;MPI_Send(&value,1,MPI_INT,1,0,MPI_COMM_WORLD);std::cout<<"rank 0 sent to rank 1\n"<<std::flush;}
 if(rank==1){int value=-1;std::cout<<"rank 1 waiting for rank 2 (no such send)...\n"<<std::flush;MPI_Recv(&value,1,MPI_INT,2,0,MPI_COMM_WORLD,MPI_STATUS_IGNORE);}
 MPI_Finalize();return 0;
}

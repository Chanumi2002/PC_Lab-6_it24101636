#include <mpi.h>
#include <iostream>
#include <vector>
int main(int argc,char** argv){
 MPI_Init(&argc,&argv);int rank,size,length;MPI_Comm_rank(MPI_COMM_WORLD,&rank);MPI_Comm_size(MPI_COMM_WORLD,&size);
 char host[MPI_MAX_PROCESSOR_NAME];MPI_Get_processor_name(host,&length);
 std::cout<<"Hello from rank "<<rank<<" of "<<size<<" on "<<host<<"\n";
 MPI_Finalize();return 0;
}

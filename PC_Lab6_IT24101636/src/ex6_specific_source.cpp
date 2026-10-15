#include <mpi.h>
#include <iostream>
// Comparison baseline for Exercise 6: receives in rank order.
int main(int argc,char** argv){
 MPI_Init(&argc,&argv);int rank,size;MPI_Comm_rank(MPI_COMM_WORLD,&rank);MPI_Comm_size(MPI_COMM_WORLD,&size);
 if(size<2){if(rank==0)std::cerr<<"Run with at least 2 processes\n";MPI_Finalize();return 1;}
 const int tag=11;
 if(rank==0){for(int source=1;source<size;++source){int value;MPI_Status status;
   MPI_Recv(&value,1,MPI_INT,source,tag,MPI_COMM_WORLD,&status);
   std::cout<<"Received "<<value<<" from rank "<<status.MPI_SOURCE<<"\n";
  }}else{int value=rank*100;MPI_Send(&value,1,MPI_INT,0,tag,MPI_COMM_WORLD);}
 MPI_Finalize();return 0;
}

#include <mpi.h>
#include <iostream>
#include <vector>
int main(int argc,char** argv){
 MPI_Init(&argc,&argv);int rank,size;MPI_Comm_rank(MPI_COMM_WORLD,&rank);MPI_Comm_size(MPI_COMM_WORLD,&size);
 if(size<2){if(rank==0)std::cerr<<"Run with at least 2 processes\n";MPI_Finalize();return 1;}
 const int tag=12;
 if(rank==0){for(int i=1;i<size;++i){int value;MPI_Status status;
   MPI_Recv(&value,1,MPI_INT,MPI_ANY_SOURCE,tag,MPI_COMM_WORLD,&status);
   std::cout<<"Received "<<value<<" from rank "<<status.MPI_SOURCE<<"\n";
  }}else{int value=rank*100;int pack=0;MPI_Pack_size(1,MPI_INT,MPI_COMM_WORLD,&pack);
   std::vector<char> buffer(static_cast<std::size_t>(pack+MPI_BSEND_OVERHEAD));
   MPI_Buffer_attach(buffer.data(),static_cast<int>(buffer.size()));
   MPI_Bsend(&value,1,MPI_INT,0,tag,MPI_COMM_WORLD);
   void* detached=nullptr;int bytes=0;MPI_Buffer_detach(&detached,&bytes);
   std::cout<<"Rank "<<rank<<" retained original value "<<value<<"\n";
  }
 MPI_Finalize();return 0;
}

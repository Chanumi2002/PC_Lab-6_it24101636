#include <mpi.h>
#include <iostream>
#include <vector>
int main(int argc,char** argv){
 MPI_Init(&argc,&argv);int rank,size;MPI_Comm_rank(MPI_COMM_WORLD,&rank);MPI_Comm_size(MPI_COMM_WORLD,&size);
 if(size<2){if(rank==0)std::cerr<<"Run with at least 2 processes\n";MPI_Finalize();return 1;}
 constexpr int count=10;constexpr int tag=5;int x[count],y[count]={};
 if(rank==0){for(int i=0;i<count;++i)x[i]=10*i;
  int pack=0;MPI_Pack_size(count,MPI_INT,MPI_COMM_WORLD,&pack);
  std::vector<char> buffer(static_cast<std::size_t>(pack+MPI_BSEND_OVERHEAD));
  MPI_Buffer_attach(buffer.data(),static_cast<int>(buffer.size()));
  MPI_Bsend(x,count,MPI_INT,1,tag,MPI_COMM_WORLD);
  // x is left untouched until the MPI buffer is detached and the send completes.
  void* detached=nullptr;int bytes=0;MPI_Buffer_detach(&detached,&bytes);
  std::cout<<"Sender original x: ";for(int v:x)std::cout<<v<<" ";std::cout<<"\n";
 }else if(rank==1){MPI_Recv(y,count,MPI_INT,0,tag,MPI_COMM_WORLD,MPI_STATUS_IGNORE);
  std::cout<<"Receiver y: ";for(int v:y)std::cout<<v<<" ";std::cout<<"\n";}
 MPI_Finalize();return 0;
}

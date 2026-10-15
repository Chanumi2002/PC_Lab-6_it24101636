#include <mpi.h>
#include <iostream>
#include <algorithm>
#include <cstdlib>
#include <iomanip>
int main(int argc,char** argv){
 MPI_Init(&argc,&argv);
 int rank,size; MPI_Comm_rank(MPI_COMM_WORLD,&rank); MPI_Comm_size(MPI_COMM_WORLD,&size);
 const long long N=10000000LL;
 const long long base=N/size, remainder=N%size;
 const long long count=base+(rank<remainder?1:0);
 const long long start=rank*base+std::min(static_cast<long long>(rank),remainder)+1;
 MPI_Barrier(MPI_COMM_WORLD); double t0=MPI_Wtime();
 long long local=0; for(long long i=start;i<start+count;++i)local+=i;
 long long total=0; MPI_Reduce(&local,&total,1,MPI_LONG_LONG,MPI_SUM,0,MPI_COMM_WORLD);
 double local_t=MPI_Wtime()-t0,max_t=0;
 MPI_Reduce(&local_t,&max_t,1,MPI_DOUBLE,MPI_MAX,0,MPI_COMM_WORLD);
 if(rank==0){std::cout<<std::setprecision(12)<<"exercise=sum,processes="<<size<<",time="<<max_t<<",result="<<total<<"\n"; if(total!=N*(N+1)/2)std::cerr<<"ERROR: incorrect total\n";}
 const int failed=(rank==0 && total!=N*(N+1)/2)?1:0;
 MPI_Finalize();return failed;
}

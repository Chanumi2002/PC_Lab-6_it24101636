#include <mpi.h>
#include <iostream>
#include <random>
#include <iomanip>
#include <algorithm>
#include <cstdint>
int main(int argc,char** argv){
 MPI_Init(&argc,&argv);
 int rank,size;MPI_Comm_rank(MPI_COMM_WORLD,&rank);MPI_Comm_size(MPI_COMM_WORLD,&size);
 constexpr long long N=10000000LL;
 long long count=N/size+(rank<N%size?1:0);
 // Independent deterministic random stream per rank; estimates can differ with process count.
 std::mt19937_64 rng(20261015ULL+static_cast<std::uint64_t>(rank)*1000003ULL);
 std::uniform_real_distribution<double> uniform(0.0,1.0);
 MPI_Barrier(MPI_COMM_WORLD);double start=MPI_Wtime();
 long long local_inside=0;
 for(long long i=0;i<count;++i){double x=uniform(rng),y=uniform(rng);if(x*x+y*y<=1.0)++local_inside;}
 long long inside=0;MPI_Reduce(&local_inside,&inside,1,MPI_LONG_LONG,MPI_SUM,0,MPI_COMM_WORLD);
 double elapsed=MPI_Wtime()-start,max_elapsed=0;MPI_Reduce(&elapsed,&max_elapsed,1,MPI_DOUBLE,MPI_MAX,0,MPI_COMM_WORLD);
 if(rank==0)std::cout<<std::setprecision(12)<<"exercise=pi,processes="<<size<<",time="<<max_elapsed<<",result="<<(4.0*inside/N)<<",inside="<<inside<<",samples="<<N<<"\n";
 MPI_Finalize();return 0;
}

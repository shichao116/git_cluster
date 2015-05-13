#!/bin/bash
#PBS -N s256rs
#PBS -l nodes=1:ppn=16:core24
#PBS -l walltime=5:00:00:00
#PBS -l pmem=1900mb
#PBS -q cygnusforce-6
#PBS -k oe
#PBS -j oe
#PBS -m abe
##PBS -V
#PBS -M jwise@gatech.edu
cd $PBS_O_WORKDIR

unset PYTHONPATH
module purge
module add intel/14.0.2 hdf5/1.8.10
module add openmpi
module list
export PATH=$HOME/local/bin:$PATH
export PYTHONPATH=$HOME/local/lib/python2.7/site-packages:$PYTHONPATH
#export LIBM_DIR=/usr/local/packages/amdlibm/3.0.2
#export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:${LIBM_DIR}/lib

output=hosts
input=$PBS_NODEFILE
ppn=$PBS_NUM_PPN
np=$PBS_NP
nn=$PBS_NUM_NODES

hosts=`cat $input | uniq`
[ -f hosts ] && rm hosts
for h in $hosts; do
    ns=`grep -c $h $input`
    ns=`expr $ns / $ppn`
    echo "$h slots=$ns" >> $output
done

[ ! -d rockstar_halos ] && mkdir rockstar_halos
[ -f rockstar_halos/auto-rockstar.cfg ] && rm -v rockstar_halos/auto-rockstar.cfg
if [ -f rockstar_halos/restart.cfg ]; then
    cfg=rockstar_halos/restart.cfg
    for i in `seq 0 100`; do
	newc=`echo $i | gawk '{printf "client%3.3d.out", $1}'`
	news=`echo $i | gawk '{printf "server%3.3d.out", $1}'`
	if [ ! -f $newc ]; then
	    cp -v client.out $newc
	    cp -v server.out $news
	    break
	fi
    done
else
    cfg=rockstar.cfg
    [ -f client.out ] && rm -v client*.out
    [ -f server.out ] && rm -v server*.out
fi

./rockstar-galaxies -c $cfg >& server.out&
echo "./rockstar-galaxies -c $cfg >& server.out&"
while [ ! -e rockstar_halos/auto-rockstar.cfg ]; do
    sleep 1
done
mpirun -n $nn --hostfile $output ./rockstar-galaxies -c rockstar_halos/auto-rockstar.cfg >& client.out
echo "mpirun -n $nn --hostfile $output ./rockstar-galaxies -c rockstar_halos/auto-rockstar.cfg >& client.out"

exit 0

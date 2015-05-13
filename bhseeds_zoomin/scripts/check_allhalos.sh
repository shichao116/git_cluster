#!/bin/bash
#----------------------------------------------------
# Example SLURM job script to run large MPI
# applications in the large queue on TACC's Stampede
# system.
#----------------------------------------------------
#SBATCH -J rockstar        # Job name
#SBATCH -o rockstar.o%j    # Name of stdout output file(%j expands to jobId)
#SBATCH -e rockstar.o%j    # Name of stderr output file(%j expands to jobId)
#SBATCH -p normal # submit to the 'large' queue for jobs > 256 nodes
#SBATCH -N 1              # Total number of nodes requested (16 cores/node)
#SBATCH -n 16             # Total number of mpi tasks requested
#SBATCH -t 48:00:00         # Run time (hh:mm:ss) - 1.5 hours
#The next line is required if the user has more than one project
# #SBATCH -A A-yourproject  # Allocation name to charge job against
export PYTHONPATH=$HOME/local/lib/python2.7/site-packages:$PYTHONPATH
module list

python check_allhalos.py >& check_allhalos.out

import numpy as np
import glob
from yt.mods import *
import pickle
target_bhs_indices = np.loadtxt('target_bhs_indices.txt')
allhaloidx1 = np.loadtxt('allhalos1.txt')
allhaloidx1 = allhaloidx1[allhaloidx1[:,31].argsort()]
DD = glob.glob('DD*/*.hierarchy')
DD.sort()
allbhsidx_r8 = []
for i in range(0,allhaloidx1.shape[0]):
    print i	
    pf = load(DD[i])
    sph = pf.h.sphere(allhaloidx1[i,17:20]/28.4, (8*allhaloidx1[i,11],'kpccm/h'))
    bhidx = []
    for j in range(target_bhs_indices.size):
        if np.any(sph['particle_index'] == target_bhs_indices[j]):
            bhidx.append(np.where(sph['particle_index'] == target_bhs_indices[j])[0][0])
    bhidx = np.array(bhidx)
    allbhsidx_r8.append(bhidx)
    
allbhsidx_r8 = np.array(allbhsidx_r8)
np.savetxt('allbhsidx_r8.txt', allbhsidx_r8)

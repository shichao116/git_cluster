import numpy as np
import glob
from yt.mods import *
import pickle
target_bhs_indices = np.loadtxt('target_bhs_indices.txt')
allhaloidx1 = np.loadtxt('allhalos1.txt')
allhaloidx1 = allhaloidx1[allhaloidx1[:,31].argsort()]
DD = glob.glob('DD*/*.hierarchy')
DD.sort()
bhsvel = []
bhspos = []
allbhsidx = []
pname = []
vname = []
for i in range(allhaloidx1.shape[0]):
    pname.append('bhpos'+str(i)+'.txt')
    vname.append('bhvel'+str(i)+'.txt')
for i in range(96,allhaloidx1.shape[0]):
    print i	
    pf = load(DD[i])
    sph = pf.h.sphere(allhaloidx1[i,17:20]/28.4, (10*allhaloidx1[i,11],'kpccm/h'))
    bhidx = []
    for j in range(target_bhs_indices.size):
        if np.any(sph['particle_index'] == target_bhs_indices[j]):
            bhidx.append(np.where(sph['particle_index'] == target_bhs_indices[j])[0][0])
    bhidx = np.array(bhidx)
    bhvel = np.array([sph['particle_velocity_x'][bhidx.astype('int')],sph['particle_velocity_y'][bhidx.astype('int')],sph['particle_velocity_z'][bhidx.astype('int')]]).T
    bhpos = np.array([sph['particle_position_x'][bhidx.astype('int')],sph['particle_position_y'][bhidx.astype('int')],sph['particle_position_z'][bhidx.astype('int')]]).T
    np.savetxt(pname[i],bhpos)
    np.savetxt(vname[i],bhvel)
    bhsvel.append(bhvel)
    bhspos.append(bhpos)
    del pf
    del sph
    
bhsvel = np.array(bhsvel)
allbhsidx = np.array(allbhsidx)
np.savetxt('allbhsidx.txt', allbhsidx)
f = open('bhsvel.pickle','wb')
pickle.dump(bhsvel,f)
f = open('bhspos.pickle','wb')
pickle.dump(bhspos,f)

"""
allbhsidx2 = []
for i in range(allhaloidx2.shape[0]):
    pf = load(DD[i])
    sph = pf.h.sphere(allhaloidx2[i,17:20]/28.4, 10*allhaloidx2[i,11]/28400)
    bhidx = []
    for j in range(target_bhs_indices.size):
        if np.any(sph['particle_index'] == target_bhs_indices[j]):
            bhidx.append(np.where(sph['particle_index'] == target_bhs_indices[j])[0][0])
    allbhsidx2.append(bhidx)

allbhsidx2 = np.array(allbhsidx2)


np.savetxt('allbhsidx2.txt', allbhsidx2)
"""

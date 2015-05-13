from yt.mods import *
from yt import YTArray
import numpy as np
import glob
import pickle
#allbhsidx = np.loadtxt('allbhsidx.txt')
f = open('bhsvel.pickle')
bhsvel = pickle.load(f)

DD  = glob.glob('DD*/*.hierarchy')
DD.sort()
allhaloidx = np.loadtxt('allhalos1.txt')

halovel = []
bhsvel_corrected = []
#ptype = []
for i in range(allhaloidx.shape[0]):
    print "index of dataset: ", i
    pf = load(DD[i])
    sp = pf.sphere(allhaloidx[i,17:20]/28.4, (allhaloidx[i,11],'kpccm/h'))
    halovel.append(sp.quantities.bulk_velocity(use_gas=True))
    bhvel = bhsvel[i]
    bhvel = YTArray(bhvel,'cm/s')
    bhvel = bhvel - halovel[-1]
    bhsvel_corrected.append(bhvel)
    #if i == 0:
    #    bhsvel_corrected = bhvel
    #else:
    #    bhsvel_corrected = np.concatenate((bhsvel_corrected,bhvel))
    #ptype.append(sp['particle_type'][allbhsidx[i].astype('int')])

bhsvel_corrected = np.array(bhsvel_corrected)
#ptype = np.array(ptype).astype('int')   
bhsvel = np.array(bhsvel)
halovel = np.array(halovel)

np.savetxt('ptype.txt',ptype)
np.savetxt('bhsvel_corrected.txt', bhsvel_corrected)
np.savetxt('halo_bulk_velocity.txt', halovel)

    

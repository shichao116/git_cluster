import yt
import numpy as np
import pickle
import glob

f = open('allindhalos')
allhalos = pickle.load(f)
f.close()

f = open('allbhs_sort_by_redshift')
allbhs = pickle.load(f)
f.close()

f = open('all_halo_bhs')
allhbhs = pickle.load(f)
f.close()

nfiles = len(allbhs)

halos_split = []
for i in range(nfiles):
    halos_split.append(allhalos[np.where(allhalos[:,31] == i)[0]])

G = 6.67259e-8
pf = yt.load('DD0173/output_0173')
conv_len_cm = float( pf.length_unit.in_cgs() )
conv_mass_g = float( pf.mass_unit)/float(pf.mass_unit.in_units('Msun/h') )

hbhs = allhbhs[-1]
bhs = allbhs[-1]
halos = halos_split[-1]
smas = np.array([])
eccs = np.array([])

for j in range(hbhs.shape[0]):
    halo = halos[hbhs[j][0][0]]
    halopos = halo[17:20]
    halovel = halo[20:23]*100000
    halomass = halo[10]*conv_mass_g
    
    bhidx = hbhs[j][1].astype('int')
    bhspos = (bhs[bhidx][:,3:6] - halopos)*conv_len_cm
    
    bhsvel = bhs[bhidx][:,6:9] - halovel
    bhsv2 = (bhsvel**2).sum(1)
    r2 = ((bhspos**2).sum(1))**0.5
    sma = np.abs((2/r2 - bhsv2/G/halomass)**(-1))
    ecc = np.array([1/r2-1/sma]).T*bhspos - np.array([(bhspos*bhsvel).sum(1)]).T*bhsvel/G/halomass    
    ecc = ((ecc**2).sum(1))**0.5
    smas = np.concatenate([smas,sma])
    eccs = np.concatenate([eccs,ecc])

smas = np.array(smas)
np.savetxt('smas_all.txt',smas)
np.savetxt('eccs_all.txt',eccs)

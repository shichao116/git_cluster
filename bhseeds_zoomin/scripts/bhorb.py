import yt
import numpy as np
import pickle
import glob

G = 6.67259e-8

allhalos = np.loadtxt('allhalos1.txt')
allhalos = allhalos[allhalos[:,31].argsort()]

pf = yt.load('DD0173/output_0173')
conv_len_cm = float( pf.length_unit.in_cgs() )
conv_mass_g = float( pf.mass_unit)/float(pf.mass_unit.in_units('Msun/h') )

halosvel = np.loadtxt('halosvel_latest.txt')


f = open('Bhspos_r8.pickle')
bhspos = pickle.load(f)
f.close()
bhspos = np.array(bhspos)

f = open('Bhsvel_r8.pickle')
bhsvel = pickle.load(f)
f.close()
for i in range(bhsvel.shape[0]):
    bhsvel[i] = bhsvel[i] - halosvel[i]

bhsv2 = (bhsvel**2).sum(2)
halopos = allhalos[:,17:20]/28.4
halomass = allhalos[:,10]*conv_mass_g 

r2 = []
bhspos_rel = []

for i in range(bhspos.shape[0]):
    bhspos_rel.append((bhspos[i] - halopos[i])*conv_len_cm)
    r2.append( (((bhspos[i] - halopos[i])**2).sum(1))**0.5 )

bhspos_rel = np.array(bhspos_rel)
r2 = np.array(r2)
r2 = r2*conv_len_cm


#semi-major axes
smas = []

for i in range(bhspos.shape[0]):
    sma = (2/r2[i]-bhsv2[i]/G/halomass[i])**(-1)
    smas.append(sma)

smas = np.array(smas)
np.savetxt('smas.txt',smas)

#eccentricity
eccs = []
for i in range(bhspos.shape[0]):
    temp =  np.array([(bhspos_rel[i]*bhsvel[i]).sum(1)]).T *bhsvel[i]/halomass[i]/G
    ecc = np.array([1/r2[i] - 1/smas[i]]).T*bhspos_rel[i] - temp
    eccs.append(ecc)

eccs = np.array(eccs)
e = ((eccs**2).sum(2))**0.5
np.savetxt('eccs.txt',e)

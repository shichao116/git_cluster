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

L  = np.zeros(bhsvel.shape)

L[:,:,0] = bhspos_rel[:,:,1]*bhsvel[:,:,2] - bhspos_rel[:,:,2]*bhsvel[:,:,1]
L[:,:,1] = bhspos_rel[:,:,2]*bhsvel[:,:,0] - bhspos_rel[:,:,0]*bhsvel[:,:,2]
L[:,:,2] = bhspos_rel[:,:,0]*bhsvel[:,:,1] - bhspos_rel[:,:,1]*bhsvel[:,:,0]


f = open('BhsL_r8.pickle','wb')
pickle.dump(L,f)

L2 = np.sqrt(np.sum(L**2,2))

np.savetxt('BhsL2_r8.txt', L2)


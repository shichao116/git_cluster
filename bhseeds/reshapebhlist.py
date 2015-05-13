import yt
import numpy as np
import pickle
import glob

f = open('rshaloanalysis/allindhalos')
allhalos = pickle.load(f)
f.close()

f = open('rshaloanalysis/allbhs_sort_by_redshift')
allbhs = pickle.load(f)
f.close()

f = open('rshaloanalysis/all_halo_bhs')
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

#smas = np.array([])
#eccs = np.array([])
allnewbhlist = []
for i in range(nfiles):
    hbhs = allhbhs[i]
    bhs = allbhs[i]
    halos = halos_split[i]
    for j in range(hbhs.shape[0]):
        halo = halos[hbhs[j][0][0]]
        halopos = halo[17:20]
        halovel = halo[20:23]*100000
        halomass = halo[10]*conv_mass_g
        
        bhidx = hbhs[j][1].astype('int')
        bhspos = (bhs[bhidx][:,3:6] - halopos)*conv_len_cm
	bhsvel = bhs[bhidx][:,6:9] - halovel
        bhspidx = bhs[bhidx][:,0]
        
        #[bhpidx(1),bhidx(1),bhpos(3),bhsvel(3),haloid(1),halomass(1),j,i]
        #x,   y,  z : 2,3,4
        #vx, vy, vz : 5,6,7
        temp = np.zeros((bhspidx.shape[0],12))
        temp[:,0] = bhspidx
        temp[:,1] = bhidx
        temp[:,2:5] = bhspos
        temp[:,5:8] = bhsvel
        temp[:,8] = hbhs[j][0][0]
        temp[:,9] = halomass
        temp[:,10] = j
        temp[:,11] = i   
        if j==0:
            newbhlist = temp;
        else:
            newbhlist = np.concatenate((newbhlist,temp))

    allnewbhlist.append(newbhlist) 

f = open('allnewbhlist.pickle','w')
pickle.dump(allnewbhlist,f)
f.close()


for i in range(nfiles):
    allnewbhlist[i] = allnewbhlist[i][allnewbhlist[i][:,0].argsort()]
    allnewbhlist[i] = np.concatenate((allnewbhlist[i],np.zeros((allnewbhlist[i].shape[0],1))),1)#last column record if this element has been visited
f = open('allnewbhlist_sorted.pickle','w')
pickle.dump(allnewbhlist,f)
f.close()

allbhstrack = []
for i in range(nfiles-1):
    bhstrack = []
    for j in range(allnewbhlist[i].shape[0]):
        found = True
        if allnewbhlist[i][j,-1] != 0:
            continue
        ii = i
        k = 0
        bhtrack = []
        while found & (ii < nfiles-1):
            print ii
            bhlist = allnewbhlist[ii]
            nextbhlist = allnewbhlist[ii+1]
            loc = np.searchsorted(nextbhlist[:,0],bhlist[j,0])
            if loc < nextbhlist.shape[0]:
                if bhlist[j,0] == nextbhlist[loc,0]:
                    if k == 0:
                        bhtrack.append(j)
                        bhtrack.append(loc)
                    else:
                        bhtrack.append(loc)
                    nextbhlist[loc,-1] = 1
                else:
                    found = False
            else:
                found = False
            ii = ii + 1
            k = k + 1
        if len(bhtrack) > 0:
            bhstrack.append(bhtrack)
        allnewbhlist[i][j,-1] = 1
    allbhstrack.append(bhstrack)

f = open('allbhstrack.pickle','w')
pickle.dump(allbhstrack, f)
f.close()

allbhsL = []
for i in range(len(allbhstrack)):
    bhstrack = allbhstrack[i]
    bhsL = []
    for j in range(len(bhstrack)):
        bhtrack = bhstrack[j]
        bhL = []
        for k in range(len(bhtrack)):
            idx = bhtrack[k]
            bhlist = allnewbhlist[i+k]
            bh = bhlist[idx]
            ang = np.array([bh[3]*bh[7]-bh[4]*bh[6], bh[4]*bh[5]-bh[2]*bh[7], bh[2]*bh[6]-bh[3]*bh[5]])
            L = (np.sum(ang**2))**0.5
            bhL.append(L)
        bhL = np.array(bhL)
        bhsL.append(bhL)
    allbhsL.append(bhsL)

f = open('allbhsL.pickle','w')
pickle.dump(allbhsL,f)
f.close()


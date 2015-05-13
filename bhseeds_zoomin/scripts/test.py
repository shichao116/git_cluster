from yt.mods import *
import glob

DD = glob.glob('DD*/*.hierarchy')
DD.sort()
allhaloidx = np.loadtxt('allhalos1.txt')

pfs = []
sps = []

for i in range(len(DD)):
    print i
    pf = load(DD[i])
    pfs.append(pf)
    sp = pf.sphere(allhaloidx[i,17:20]/28.4, (allhaloidx[i,11],'kpccm/h'))
    sps.append(sp)


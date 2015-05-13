from yt.mods import *
import yt
yt.enable_parallelism()

import numpy as np
import glob
import pickle

DD = glob.glob('DD*/*.hierarchy')
DD.sort()
DD = DD[0:102]
allhaloidx = np.loadtxt('allhalos1.txt')

my_storage = {}

I = range(len(DD))

for sto, i in yt.parallel_objects(I, 16, storage = my_storage):
    pf = load(DD[i])
    sto.result_id = DD[i]
    err = 1
    c = allhaloidx[i,17:20]/28.4
    r = allhaloidx[i,11]
    while err > 1e-8:
        oc = c
        r = 0.95*r
        sp = pf.sphere(c,(r,'kpccm/h'))
        c = np.array(sp.quantities.center_of_mass(use_gas = True, use_particles = True))
        err = np.sqrt(np.sum((c-oc)**2))
    sto.result = c

itercenter = []
if yt.is_root():
    for i,vals in sorted(my_storage.items()):
        itercenter.append(vals)
    itercenter = np.array(itercenter)
    np.savetxt('itercenter.txt', itercenter)


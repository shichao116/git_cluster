from yt.mods import *
import yt
yt.enable_parallelism()

from yt import YTArray
import numpy as np
import glob
import pickle

DD  = glob.glob('DD*/*.hierarchy')
DD.sort()
DD = DD[0:102]
allhaloidx = np.loadtxt('allhalos1.txt')

my_storage = {}

I = range(len(DD))
for sto, i in yt.parallel_objects(I, 16, storage = my_storage):
    pf = load(DD[i])
    sto.result_id = DD[i]
    sp = pf.sphere(allhaloidx[i,17:20]/28.4, (allhaloidx[i,11], 'kpccm/h'))
    sto.result = sp.quantities.bulk_velocity(use_gas=True)

halosvel = []
if yt.is_root():
    for i,vals in sorted(my_storage.items()):
        halosvel.append(vals)
    halosvel = np.array(halosvel)
    np.savetxt('halosvel_latest.txt',halosvel) 
   

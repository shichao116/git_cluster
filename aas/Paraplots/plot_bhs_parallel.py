from yt.mods import *
import yt
yt.enable_parallelism()

from yt import YTArray
import numpy as np
import glob
import pickle

f = open('../Bhspos_r8.pickle')
bhspos = pickle.load(f)
f.close()

DD  = glob.glob('../DD*/*.hierarchy')
DD.sort()
DD = DD[0:102]
allhaloidx = np.loadtxt('../allhalos1.txt')

my_storage = {}

I = range(len(DD))
for sto, i in yt.parallel_objects(I, 16, storage = my_storage):
    pf = load(DD[i])
    sto.result_id = DD[i]
    sto.result = []
    sp = pf.sphere(allhaloidx[i,17:20]/28.4, (8*allhaloidx[i,11], 'kpccm/h'))
    proj = ProjectionPlot(pf,'y','Density', center = allhaloidx[i,17:20]/28.4, width = 20*allhaloidx[i,11]/28400, data_source = sp)
    for j in range(bhspos[i].shape[0]):
        proj.annotate_marker([bhspos[i][j][0],bhspos[i][j][1],bhspos[i][j][2]],marker='o')
    proj.save()




    

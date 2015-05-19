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

c = allhaloidx[0,17:20]/28.4
r = (3*allhaloidx[0,11],'kpccm/h')

my_storage = {}

I = range(len(DD))
for sto, i in yt.parallel_objects(I, 16, storage = my_storage):
    pf = load(DD[i])
    sto.result_id = DD[i]
    sto.result = []
    sp = pf.sphere(c, r)
    proj = ProjectionPlot(pf,'y','Density', center = c, width = (6*allhaloidx[0,11],'kpccm/h'), data_source = sp)
    for j in range(bhspos[i].shape[0]):
        proj.annotate_marker([bhspos[i][j][0],bhspos[i][j][1],bhspos[i][j][2]],marker='o')
    proj.save()

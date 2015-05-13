from yt.mods import *
from yt import YTArray
import numpy as np
import glob
import pickle

f = open('Bhspos_r8.pickle')
bhspos = pickle.load(f)

DD  = glob.glob('DD*/*.hierarchy')
DD.sort()
allhaloidx = np.loadtxt('allhalos1.txt')



for i in range(allhaloidx.shape[0]):
    pf = load(DD[i])
    sp = pf.sphere(allhaloidx[i,17:20]/28.4, (8*allhaloidx[i,11], 'kpccm/h'))
    proj = ProjectionPlot(pf,'y','Density', center = allhaloidx[i,17:20]/28.4, width = 20*allhaloidx[i,11]/28400, data_source = sp)
    for j in range(bhspos[i].shape[0]):
        proj.annotate_marker([bhspos[i][j][0],bhspos[i][j][1],bhspos[i][j][2]],marker='o')
    proj.save()
    del proj

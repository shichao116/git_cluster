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
allhaloidx = np.loadtxt('../allhalos1.txt')

my_storage = {}

print len(DD)
I = range(len(DD))
for sto, i in yt.parallel_objects(I, 16, storage = my_storage):
    pf = load(DD[i])
    sto.result_id = DD[i]
    sto.result = i

if yt.is_root():
    for i, vals in sorted(my_storage.items()):
        print i, vals
   

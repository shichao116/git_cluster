import matplotlib.pyplot as plt
#from matplotlib.backends.backend_pdf import PdfPages
import numpy as np


eccs = np.loadtxt('eccs_all.txt')
idx = np.where(eccs < 1)[0]
eccss = eccs[idx]
smas = np.loadtxt('smas_all.txt')
smass = smas[idx]

#fig = plt.figure(figsize = (27,12), dpi = 240)
#pp = PdfPages('bhsorb.pdf')
plt.subplot(121)
n, bins, patches = plt.hist(eccss, 50)
plt.subplot(122)
n, bins, patches = plt.hist(smass, 50)

plt.savefig('bhsorb')


  

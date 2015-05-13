import glob
import numpy as np
import pickle

fbpos = glob.glob('bhpos*.txt');fbpos.sort()
fbvel = glob.glob('bhvel*.txt');fbvel.sort()
border = np.array([int(fbpos[i][5:-4]) for i in range(len(fbpos))])
border = border[border.argsort()]

fhvel = glob.glob('halovel*.txt');fhvel.sort()
forder = np.array([int(fhvel[i][7:-4]) for i in range(len(fhvel))])
forder = forder[forder.argsort()]

bhspos = []
bhsvel = []
halosvel = []

for i in range(len(fbpos)):
    bhspos.append(np.loadtxt(fbpos[i]))
    bhsvel.append(np.loadtxt(fbvel[i]))
    halosvel.append(np.loadtxt(fhvel[i]))

bhspos = np.array(bhspos)
bhsvel = np.array(bhsvel)
halosvel = np.array(halosvel)

f = open('bhspos.pickle','w')
pickle.dump(bhspos,f)
f.close()

f = open('bhsvel.pickle2','w')
pickle.dump(bhsvel,f)
f.close()

np.savetxt('halosvel.txt',halosvel)

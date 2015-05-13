from yt.mods import *
from yt.analysis_modules.halo_finding.rockstar.api import RockstarHaloFinder
import glob
import numpy as na
nmax = None

@particle_filter("finest", ["particle_mass", "particle_type"])

def finest(pfilter, data):
    return ((data["particle_mass"].in_units("Msun") < 5e4) &
            (data["particle_mass"].in_units("Msun") > 1e3) & 
            (data["particle_type"] == 1))

#find all of our simulation files
files = glob.glob("../DD*/*hierarchy")
#files += glob.glob("DD0046/*hierarchy")
#files += glob.glob("DD02*/*hierarchy")
#files += glob.glob("RD*/*hierarchy")

#files = ["DD0003/output_0003", "DD0004/output_0004"]
files.sort()

#sort the filelist by time
nfiles = len(files)
if nmax == None: nmax = nfiles
times = na.zeros(nfiles)
tmp = []
for i,f in enumerate(files[:]):
    pf = load(f)
    times[i] = pf.current_time
    tmp.append(pf)
isort = times.argsort()
pfs = []
nmax = min(nmax, nfiles)
for i in range(nfiles-nmax,nfiles):
    pfs.append(tmp[isort[i]])
ts = TimeSeriesData(pfs)
rh = RockstarHaloFinder(ts, num_readers=32, particle_type='finest',
                        total_particles=322375680, particle_mass=28807.25*0.71,
                        force_res=8.4638e-7)
rh.run(restart=False)


import glob, os
import yt
import numpy as np

restart_snap = None  # filename of the first dataset in the restart
                     # (None for no restart)
rockstar_base_cfg = "rockstar_base.cfg"
rockstar_cfg = "rockstar.cfg"
outbase = "rockstar_halos"
n_nodes = 1
n_procs = 16
n_readers = 2

# Create file with parameter files, sorted by time.
filename = "pfs.dat"
bases = [["DD", "output_"],
         ["DD", "data"],
         ["DD", "DD"],
         ["RD", "RedshiftOutput"],
         ["RS", "restart"]]
all_files = []
for b in bases:
    all_files += glob.glob("%s????/%s????" % (b[0], b[1]))
times = np.zeros(len(all_files))
scale = np.zeros(len(all_files))
for i,f in enumerate(all_files):
    ds = yt.load(f)
    times[i] = ds.current_time.in_units('code_time')
    scale[i] = 1.0 / (ds.current_redshift+1)
isort = np.argsort(times)
times = times[isort]
scale = scale[isort]
files = []
for i in isort:
    files.append(all_files[i])
fp = open(filename, "w")
for i,f in enumerate(files):
    #fp.write("%s %15.12f\n" % (f, scale[i]))
    fp.write("%s\n" % (f))
fp.close()

if not os.path.exists(outbase):
    os.mkdir(outbase)

# Find the number of the restart snapshot
if restart_snap == None:
    restart_num = 0
else:
    if files.count(restart_snap) == 0:
        raise RuntimeError("restart snapshot %s not found" % (restart_snap))
    else:
        restart_num = files.index(restart_snap)

# Find the finest proper resolution (use the last snapshot only)
ds = yt.load(files[-1])
dx_min = ds.index.get_smallest_dx().in_units("Mpccm/h")

# Determine whether a zoom-in simulation
zoom_in = "StaticRefineRegionLevel[0]" in ds.parameters

# Write rockstar config file
lines = open(rockstar_base_cfg, "r").readlines()
fp = open(rockstar_cfg, "w")
for l in lines:
    fp.write(l)
fp.write("OUTBASE = %s\n" % (outbase))
fp.write("NUM_BLOCKS = %d\n" % (n_readers))
fp.write("NUM_WRITERS = %d\n" % (n_procs))
fp.write("FORK_PROCESSORS_PER_MACHINE = %d\n" % (n_procs/n_nodes))
fp.write("SNAPSHOT_NAMES = %s\n" % (filename))
#fp.write("NUM_SNAPS = %d\n" % (len(files)))
#fp.write("STARTING_SNAP = %d\n" % (restart_num))
fp.write("FORCE_RES = %g\n" % (dx_min))
fp.write("PERIODIC = %d\n" % (not zoom_in))
fp.write("ENZO_ZOOMIN_RESTRICT = %d\n" % (zoom_in))
fp.close()

import os
import shutil
import sys
from subprocess import call
#from obspy import read
#import scipy.io as sio

#path_in = '../data_40kHz/'
#path_in = '../data_40kHz_free_sides/'
#path_in = '../data_100kHz/'
path_in = '../data_100kHz_free_sides/'
#path_out = '../data_40kHz_polluted/'
#path_out = '../data_40kHz_free_sides_polluted/'
#path_out = '../data_100kHz_polluted/'
path_out = '../data_100kHz_free_sides_polluted/'
if not os.path.exists(path_out):
    os.makedirs(path_out)


#****************************************************************************
# Data description
#****************************************************************************
nshots_x = 10
nshots_y = 1
nshots = nshots_x * nshots_y

sinc_x = 1 
sinc_y = 1

dl = 1
tsteps = 2400 #1800
dt = 5.0e-5

comp1 = 'Uz'
comp2 = 'Ux'
sn = 1

shot_y = 1
shot_sta = (shot_y-1)*nshots_x
shot_fin = shot_y*nshots_x


#****************************************************************************
# loop over shots and add noise to traces
#****************************************************************************
for shot_x in range(shot_sta,shot_fin):
    dz_src = path_in  + str(shot_x).zfill(6) + '/' + comp1 + '_file_single.su'
    dx_src = path_in  + str(shot_x).zfill(6) + '/' + comp2 + '_file_single.su'
    dest = path_out + str(shot_x).zfill(6)
    if not os.path.exists(dest):
    	os.makedirs(dest)
    dz_dest = path_out  + str(shot_x).zfill(6) + '/' + comp1 + '_file_single.su'
    dx_dest = path_out  + str(shot_x).zfill(6) + '/' + comp2 + '_file_single.su'

    #shutil.copyfile(dz_src,dz_dest)
    #shutil.copyfile(dx_src,dx_dest)

    cmd = 'suoldtonew < ' + dz_src + ' n2=80 | suaddnoise sn=50 f=900,1000,2000,2100 amps=0,1,1,0 | suswapbytes format=0 > ' + dz_dest
    print cmd
    call(cmd,shell=True)

    print 'shot number: ' + str(shot_x)


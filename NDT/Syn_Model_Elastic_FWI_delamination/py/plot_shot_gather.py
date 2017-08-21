import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure, show, axes, sci
from matplotlib import cm, colors
from matplotlib.font_manager import FontProperties
from numpy import amin, amax, ravel
from numpy.random import rand
from obspy import read
import scipy.io as sio

#def on_press(event):
#    if event.inaxes is None: return
#    for line in event.inaxes.lines:
#        if event.key=='t':
#            visible = line.get_visible()
#            line.set_visible(not visible)
#    event.inaxes.figure.canvas.draw()

#path_in = '../data_40kHz/000004/'
#path_in = '../data_40kHz_polluted/000004/'
#path_in = '../data_100kHz/000004/'
path_in = '../data_100kHz_polluted/000004/'
trace_type = '' #'obs'/'syn'/'adj'
path_out = '../figs/'
if not os.path.exists(path_out):
    os.makedirs(path_out)


#****************************************************************************
# Data description
#****************************************************************************
nrecs_x = 10
nrecs_y = 1
nrecs = nrecs_x * nrecs_y
#rcvr_global_1x = 76
#rcvr_global_1y = 51

rinc_x = 1
rinc_y = 1
#x0 = int(rcvr_global_1x)
#y0 = int(rcvr_global_1y)

dl = 1
tsteps = 2400 #1800
dt = 5.0e-5


#****************************************************************************
# input
#****************************************************************************
data_plot = np.zeros ((nrecs_x, tsteps))
#dat_type = 'semd'
comp1 = 'Uz'
comp2 = 'Ux'
sn = 1
prec = 'single'

rec_y = 1
rec_sta = (rec_y-1)*nrecs_x
rec_fin = rec_y*nrecs_x
rec_buf = rec_fin - rec_sta

if trace_type == 'adj':
    file_name_dz = path_in + '/' +  comp1 + '_file_single.su.adj'
    file_name_dx = path_in + '/' +  comp2 + '_file_single.su.adj'
else:
    file_name_dz = path_in + '/' +  comp1 + '_file_single.su'
    file_name_dx = path_in + '/' +  comp2 + '_file_single.su'

traces_z = read(file_name_dz)
#traces_x = read(file_name_dx)

index = 0
for rec_x in range(rec_sta,rec_fin):

    xz1 = traces_z[rec_x].data
    #xz2 = traces_x[rec_x].data

    data_plot[index,:] = xz1

    print 'rec. num. ' + str(rec_x)
    index += 1

x1 = 0
x2 = nrecs_x
t1 = 0
#t1 = 400
t2 = tsteps
drec = dl * rinc_x
data = data_plot[x1:x2,t1:t2]


##****************************************************************************
# Plot pcolor/pcolormesh
##****************************************************************************
# number of plots (rows and columns)
Nr = 1
Nc = 1

fig = figure(figsize=(5, 5))
cmap = cm.seismic

#**************
# title
#**************
#figtitle = 'Vs vertical slices'
#t = fig.text(0.5, 0.95, figtitle,
#             horizontalalignment='center',
#             fontproperties=FontProperties(size=18))

#**************
# create axis
#**************
#x_axis, y_axis = np.mgrid [x1:x2*drec:drec, t1:t2*dt:dt]
x_axis, y_axis = np.mgrid [x1*drec:x2*drec:drec, t1*dt:t2*dt:dt]

w = 0.8
h = 0.8
ax = []
images = []
vmin = 1e40
vmax = -1e40

for i in range(Nr):
    for j in range(Nc):
        pos = [0.18 + j*1.1*w, 0.12 + i*1.1*h, w, h]
        
        a = fig.add_axes(pos)
        if i > 0:
            a.set_xticklabels([])
        
        dd = ravel(data)
        
        # Manually find the min and max of all colors for
        # use in setting the color scale.
        if i == 0:
            vmax = max(vmax, amax(dd))/5
            vmin = -vmax

        images.append(a.pcolormesh(x_axis, y_axis, data, cmap=cmap))
        
        # axis
        #plt.axis([x1,(x2-1)*drec, t1, (t2-1)*dt])
        plt.axis([x1*drec,(x2-1)*drec, t1*dt, (t2-1)*dt])
        a.invert_yaxis()
        
        ## labels
        if i == 0:
            plt.xlabel('Receiver number',fontsize=16)
            #plt.xlabel('X-distance (m)',fontsize=16)
        plt.ylabel('Time (s)',fontsize=16)
        ax.append(a)


# Set the first image as the master, with all the others
# observing it for changes in cmap or norm.

class ImageFollower:
    'update image in response to changes in clim or cmap on another image'
    def __init__(self, follower):
        self.follower = follower
    def __call__(self, leader):
        self.follower.set_cmap(leader.get_cmap())
        self.follower.set_clim(leader.get_clim())

norm = colors.Normalize(vmin=vmin, vmax=vmax)
for i, im in enumerate(images):
    im.set_norm(norm)
    if i > 0:
        images[0].callbacksSM.connect('changed', ImageFollower(im))

#**************
# Colorbar
#**************
## The colorbar is also based on this master image.
#cax = fig.add_axes([0.82, 0.25, 0.025, 0.5])
#fig.colorbar(images[0], cax, orientation='vertical')


# We need the following only if we want to run this interactively and
# modify the colormap:

axes(ax[0])     # Return the current axes to the first one,
sci(images[0])  # because the current image must be in current axes.

#**************
# save fig
#**************

#plt.savefig(path_out + 'displ_40kHz_pure'  +  '.png',figsize=(8,6),dpi=300)
#plt.savefig(path_out + 'displ_40kHz_polluted'  +  '.png',figsize=(8,6),dpi=300)
#plt.savefig(path_out + 'displ_100kHz_pure'  +  '.png',figsize=(8,6),dpi=300)
plt.savefig(path_out + 'displ_100kHz_polluted'  +  '.png',figsize=(8,6),dpi=300)

#sio.savemat(path_out + 'displ_40kHz_pure'  + '.mat', {'sim_data':data})
#sio.savemat(path_out + 'displ_40kHz_polluted'  + '.mat', {'sim_data':data})
#sio.savemat(path_out + 'displ_100kHz_pure'  + '.mat', {'sim_data':data})
sio.savemat(path_out + 'displ_100kHz_polluted'  + '.mat', {'sim_data':data})

show()

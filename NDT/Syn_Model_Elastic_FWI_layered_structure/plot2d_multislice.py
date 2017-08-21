#!/usr/bin/env python

import sys
from os.path import exists
import numpy as np
import pylab
import scipy.interpolate


def read_fortran(filename):
    """ Reads Fortran style binary data and returns a numpy array.
    """
    with open(filename, 'rb') as f:
        # read size of record
        f.seek(0)
        n = np.fromfile(f, dtype='int32', count=1)[0]

        # read contents of record
        f.seek(4)
        v = np.fromfile(f, dtype='float32')

    return v[:-1]

def read_multislice(model, NSLICE, parameter):
    """ Reads NSLICE slices of the model using read_fortran(filename)
    """
    x_coords_all = np.empty(shape=(0, 0))
    z_coords_all = np.empty(shape=(0, 0))
    model_all = np.empty(shape=(0, 0))

    for si in range(NSLICE):
	file_x = model + '/proc' + str(si).zfill(6) + '_x.bin'
	file_z = model + '/proc' + str(si).zfill(6) + '_z.bin'
	file_d = model + '/proc' + str(si).zfill(6) + '_' + parameter + '.bin'

	# check that files actually exist
	assert exists(file_x), file_x + ' does not exist'
    	assert exists(file_z), file_z + ' does not exist'
    	assert exists(file_d), file_d + ' does not exist'

	x_coords = read_fortran(file_x)
	z_coords = read_fortran(file_z)
	model_slice = read_fortran(file_d)

    	x_coords_all = np.append(x_coords_all,x_coords[:])
    	z_coords_all = np.append(z_coords_all,z_coords[:])
    	model_all = np.append(model_all,model_slice[:])

    # check mesh dimensions
    assert x_coords_all.shape == z_coords_all.shape == model_all.shape, 'Inconsistent mesh dimensions.'

    return x_coords_all, z_coords_all, model_all


def mesh2grid(v, x, z):
    """ Interpolates from an unstructured coordinates (mesh) to a structured 
        coordinates (grid)
    """
    lx = x.max() - x.min()
    lz = z.max() - z.min()
    nn = v.size
    mesh = _stack(x, z)

    nx = np.around(np.sqrt(nn*lx/lz))
    nz = np.around(np.sqrt(nn*lz/lx))
    dx = lx/nx
    dz = lz/nz

    # construct structured grid
    x = np.linspace(x.min(), x.max(), nx)
    z = np.linspace(z.min(), z.max(), nz)
    X, Z = np.meshgrid(x, z)
    grid = _stack(X.flatten(), Z.flatten())

    # interpolate to structured grid
    V = scipy.interpolate.griddata(mesh, v, grid, 'nearest') # 'linear'

    # workaround edge issues
    if np.any(np.isnan(V)):
        W = scipy.interpolate.griddata(mesh, v, grid, 'nearest')
        for i in np.where(np.isnan(V)):
            V[i] = W[i]

    print 'nz =', nz
    print 'nx =', nx
    return np.reshape(V, (nz, nx))
    


def _stack(*args):
    return np.column_stack(args)



if __name__ == '__main__':
    """ Plots data on 2-D unstructured mesh

      Can be used to plot models or kernels created by SPECFEM2D

      SYNTAX
          plot2d_multislice.py  model  NSLICE parameter
      EXAMPLE
          ./plot2d_multislice.py  model_true  4  vs
    """

    # parse command line arguments
    model = sys.argv[1]
    NSLICE = int(sys.argv[2])
    parameter = sys.argv[3]


    # read all model slices
    x, z, v = read_multislice(model,NSLICE,parameter)

    # interpolate to uniform rectangular grid
    V = mesh2grid(v, x, z)

    # display figure
    fig, ax = pylab.subplots()
    pylab.pcolor(V[:,:])
    #pylab.pcolor(V[30:-30,:])
    #pylab.pcolor(V,vmin=0, vmax=5800)
    #pylab.imshow(V,vmin=2150, vmax=5800, extent=(x.min(), x.max(), z.min(), z.max())) # for Vp
    #pylab.imshow(V,vmin=0, vmax=2800, extent=(x.min(), x.max(), z.min(), z.max())) # for Vs
    pylab.axes().set_aspect('equal')
    #ax.set_ylim(0.20,0)
    pylab.xlabel('x [m]')
    pylab.ylabel('z [m]')
    pylab.colorbar(orientation='horizontal',label=parameter)
    pylab.show()


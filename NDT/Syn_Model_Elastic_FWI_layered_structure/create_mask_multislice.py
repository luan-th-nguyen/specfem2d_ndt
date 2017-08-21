#!/usr/bin/env python

import sys
import os
from os.path import isdir, exists
import numpy as np
import pylab
import scipy.interpolate
from scipy.signal import convolve2d
from seisflows.tools.math import gauss2


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



def write_fortran(filename,v):
  """ Writes Fortran style binary files--data are written as single precision
      floating point numbers
  """
  n = np.array([4*len(v)], dtype='int32')
  v = np.array(v, dtype='float32')

  with open(filename, 'wb') as file:
    n.tofile(file)
    v.tofile(file)
    n.tofile(file)
  return


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
    """ Interpolates from an unstructured coordinates (mesh) to a structured coordinates (grid)
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
    


def grid2mesh(V, x, z):
    """ Interpolates from a structured coordinates (grid) to an unstructured coordinates (mesh)
    """
    lx = x.max() - x.min()
    lz = z.max() - z.min()
    nn = V.size
    mesh = _stack(x, z)

    nx = np.around(np.sqrt(nn*lx/lz))
    nz = np.around(np.sqrt(nn*lz/lx))
    dx = lx/nx
    dz = lz/nz

    # construct structured grid
    x = np.linspace(x.min(), x.max(), nx)
    z = np.linspace(z.min(), z.max(), nz)
    X, Z = np.meshgrid(x, z)
    V = V.flatten()
    grid = _stack(X.flatten(), Z.flatten())

    # interpolate to structured grid
    v = scipy.interpolate.griddata(grid, V, mesh, 'nearest') # 'linear'

    print 'number of interpolated data points =', v.size
    return v



def gridsmooth(v,span,kernel='gauss'):
    span = np.array([span, span])
    if kernel=='gauss':
	XY = np.meshgrid(range(-2*span[0],2*(span[0]+1),2),range(-2*span[1],2*(span[1]+1),2))
	X, Y = XY[0], XY[1]
	sigma = np.diag(span**2)
	K = gauss2(X,Y,np.array([0, 0]),sigma)
        K = K/np.sum(K)

    w = np.ones(v.shape)
    v_sm = convolve2d(v,K,mode='same')
    w_sm = convolve2d(w,K,mode='same')

    return np.divide(v_sm,w_sm)

def _stack(*args):
    return np.column_stack(args)


if __name__ == '__main__':
    """ Plots data on 2-D unstructured mesh

      Can be used to plot models or kernels created by SPECFEM2D

      SYNTAX
          create_mask_multislice  model_in mask_out  NSLICE parameter
      EXAMPLE
          ./create_mask_multislice.py  model_true  model_mask 4  vs
    """

    # parse command line arguments
    model_in = sys.argv[1]
    mask_out = sys.argv[2]
    NSLICE = int(sys.argv[3])
    parameter = sys.argv[4]


    # read all model slices
    x, z, v = read_multislice(model_in,NSLICE,parameter)

    # interpolate to uniform rectangular grid
    V = mesh2grid(v, x, z)

    # create mask and smoothing
    #V_sm = gridsmooth(V,4)  # test smoothing the true model itself
    v_mask = np.ones(v.shape)
    z_idx = np.where(z > 175)
    v_mask[z_idx] = 0.0
    V_mask = mesh2grid(v_mask, x, z)
    V_mask_smooth = gridsmooth(V_mask,4) 	  # smoothed mask on grid (because convolution is done on a structured grid)
    v_mask_smooth = grid2mesh(V_mask_smooth,x,z)  # smoothed mask on mesh (for saving back to slices)

    # save mask into slices
    if isdir(mask_out)==False:
	os.mkdir(mask_out)

    x_all = np.empty(shape=(0, 0))
    z_all = np.empty(shape=(0, 0))
    v_all = np.empty(shape=(0, 0))
    pointer = 0
    for si in range(NSLICE):
	file_x = model_in + '/proc' + str(si).zfill(6) + '_x.bin'
	file_z = model_in + '/proc' + str(si).zfill(6) + '_z.bin'
	file_v = model_in + '/proc' + str(si).zfill(6) + '_' + parameter + '.bin'

	x = read_fortran(file_x)
	z = read_fortran(file_z)
	v = read_fortran(file_v)
	v_length = v.size

    	x_all = np.append(x_all,x[:])
    	z_all = np.append(z_all,z[:])
    	v_all = np.append(v_all,v[:])

	file_mask_x = mask_out + '/proc' + str(si).zfill(6) + '_x.bin'
	file_mask_z = mask_out + '/proc' + str(si).zfill(6) + '_z.bin'
	file_mask_v = mask_out + '/proc' + str(si).zfill(6) + '_' + parameter + '.bin'
	write_fortran(file_mask_x,x)
	write_fortran(file_mask_z,z)
	write_fortran(file_mask_v,v_mask_smooth[pointer:pointer+v_length])  # write out a mask slice

	pointer += v_length
    

    # display figure
    fig, ax = pylab.subplots()
    pylab.pcolor(V_mask_smooth[:,:])
    pylab.axes().set_aspect('equal')
    #ax.set_ylim(0.20,0)
    pylab.xlabel('x [m]')
    pylab.ylabel('z [m]')
    pylab.colorbar(orientation='horizontal',label=parameter)
    pylab.show()


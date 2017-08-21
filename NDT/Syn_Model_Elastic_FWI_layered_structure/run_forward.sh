#!/bin/bash
#
# script runs mesher and solver (in serial)
# using this example setup
#

#echo "running example: `date`"
rundir=`pwd`

cd $rundir

mkdir -p OUTPUT_FILES

# links executables
rm -f xmeshfem2D xspecfem2D
ln -s ../../bin/xmeshfem2D
ln -s ../../bin/xspecfem2D

# sets up local DATA/ directory
#cd DATA/
#cp -f ../Par_file_true Par_file
#cp -f ../interfaces.dat ./
#cd ../

echo
echo "(SPECFEM2D starts)"
echo

# runs database generation
echo
echo "  running mesher..."
echo
./xmeshfem2D > OUTPUT_FILES/output_mesher.txt

# runs simulation
echo
echo "  running solver..."
echo
#./xspecfem2D > OUTPUT_FILES/output_solver.txt
mpirun -np 4 ./xspecfem2D > OUTPUT_FILES/output_solver.txt

echo
echo "see results in directory: OUTPUT_FILES/"
echo
echo "done"
echo `date`

#python plot_seismogram_dxz.py

##mogrify -resize 800x800 OUTPUT_FILES/*.jpg
##convert OUTPUT_FILES/*.jpg OUTPUT_FILES/%03d.jpg
##ffmpeg -r 8 -qscale 2 -i OUTPUT_FILES/%03d.jpg OUTPUT_FILES/movie_waves.mp4




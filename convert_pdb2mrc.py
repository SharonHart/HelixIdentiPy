"""
This script is for converting a .pdb file to .mrc file.
EMAN2 needs to be installed on your system
1) Download a pdb file from http://www.rcsb.org/
2) Change to your python27 location
3) Change to your e2pdb2mrc script location (I recommend using "Everything" to find the files quickly: https://www.voidtools.com/)
4) Change target_file_location to the desired location of the output file

* you can than open the file in Chimera to see that it worked
"""
import numpy
from EMAN2 import *
import os
from numpy.core.multiarray import ndarray

python_location = "C:\\EMAN2\\python\\Python27\\python.exe "
e2pdb2mrc_location = "C:\\EMAN2\\bin\\e2pdb2mrc.py "
pdb_file_location = "C:\\Users\\guloo\\Downloads\\4xnh.pdb "
target_file_location = "C:/Users/guloo/Desktop/out.mrc"
os.system(python_location + e2pdb2mrc_location + pdb_file_location + target_file_location)

from TEMPy.MapParser import *
from TEMPy.ScoringFunctions import *
import scipy.signal as sps

input_path = "/home/guloo/Downloads/emd_1094.map"
cylinder_path = "/home/guloo/Downloads/Cylinder.mrc"

print("Parsing maps...")
target_map = MapParser.readMRC(input_path)
cylinder_map = MapParser.readMRC(cylinder_path)

print("Cropping Ideal cylinder...")
nparr = cylinder_map.fullMap
nparr = nparr[50:57, 47:54, 47:54] # shape: 7X7X7


print("Building correlation matrix...")
correlation_matrix = sps.correlate(nparr, target_map.fullMap, mode="valid")


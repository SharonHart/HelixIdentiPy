from TEMPy.MapParser import *
from TEMPy.ScoringFunctions import *
import scipy.signal as sps

input_path = "./source/emd_1094.map"
cylinder_path = "./source/Cylinder.mrc"
target_map = MapParser.readMRC(input_path)
cylinder_map = MapParser.readMRC(cylinder_path)

# get small matrix of
nparr = cylinder_map.fullMap
nparr = nparr[50:57, 47:54, 47:54] # shape: 7X7X7

a = sps.correlate(target_map.fullMap, nparr, mode="valid")


print(a.shape)
print(a.max())

t = target_map.change_origin(0,0,0)
print(t.origin)
print(t.box_size())
cylinder_map = cylinder_map.resize_map((60,60,60))
print (target_map.box_size())

s = ScoringFunctions()

score = s.CCC(cylinder_map, t)

print ("score:{} ".format(score))
print(t.origin)
# print(c.origin)
# print(t.box_size())
# print(c.box_size())
#
# score = s.SCCC(t, c)
# print ("score:{} ".format(score[0]))
#
# arr =  target_map.fullMap
#
# x_len, y_len, z_len = arr.shape
#
# for x in range (x_len):
#     for y in range (y_len):
#         for z in range (z_len):
#             cylinder_map.translate(x,y,z)
#             score = ScoringFunctions.CCC(target_map, cylinder_map)
#             print score
# pass

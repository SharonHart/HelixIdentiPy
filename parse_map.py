from TEMPy.MapParser import *
from TEMPy.ScoringFunctions import *
from TEMPy.StructureBlurrer import *
from scipy.ndimage.filters import gaussian_filter
from scipy.signal import correlate
import numpy as np

input_path = "./source/emd_1094.map"
cylinder_path = "./source/Cylinder.mrc"
target_map = MapParser.readMRC(input_path)
cylinder_map = MapParser.readMRC(cylinder_path)

# trim cylinder to it smallest form
cylinder_array = cylinder_map.fullMap
cylinder_array = cylinder_array[50:57, 47:54, 47:54] # shape: 7X7X7

# smooth cylinder by gaussian mask TODO: figure out how to get sigma
sigma = target_map.apix
cylinder_array = gaussian_filter(cylinder_array, sigma)

cylinder_map.fullMap = cylinder_array

max_scores = np.zeros(target_map.box_size())
max_dirs = np.zeros(target_map.box_size(), dtype=(float,2))


sanity = 0
rad_in_x = 0 # accumulate rotation in the x axis (in rads)
for i in range (12): #for every x rotation
    rad_in_x += (math.pi/12) * i
    rad_in_y = 0 #accumulate rotation in the y axis (in rads)
    for j in range (12): #for every y rotation
        rad_in_y += (math.pi/12) * j
        template_cylinder = cylinder_map
        template_cylinder.rotate_by_axis_angle(x=1, y=0, z=0, angle=rad_in_x, CoM=cylinder_map.centre(), rad=True)
        template_cylinder.rotate_by_axis_angle(x=0, y=1, z=0, angle=rad_in_y, CoM=cylinder_map.centre(), rad=True)
        correlation_matrix = correlate(target_map.fullMap, template_cylinder.fullMap, mode="same")
        # scipy correlate is super-slow :(
        for (x,y,z), value in np.ndenumerate(correlation_matrix):
            if value > max_scores[x,y,z]:
                max_scores[x,y,z] = value
                max_dirs[x,y,z] = (rad_in_x, rad_in_y)

        sanity += 1
        print sanity

print max_scores
print max_dirs


#score = s.CCC(cylinder_map, t)

#print ("score:{} ".format(score))
#print(t.origin)
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

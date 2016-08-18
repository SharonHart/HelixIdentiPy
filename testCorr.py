import numpy as np
from TEMPy.MapParser import *
from TEMPy.ScoringFunctions import *
from scipy.ndimage.interpolation import shift as shifta

import os
from messages import Messages
from norm_xcorr import norm_xcorr
from sklearn.cross_decomposition import CCA
""""Correlates between the target and the generated templates. Returns score matrix and direction matrix"""

target_path = sys.argv[1]

target_map = MapParser.readMRC(target_path)
ones_map = np.ones(target_map.fullMap.shape)
target_map.fullMap=ones_map
a = target_map.apix
print target_map.centre()
target_map.fullMap = shifta(target_map.fullMap, [0, 0, -1])
print target_map.fullMap
print target_map.fullMap.min()

#
# sanity = 0
#
# for i in range(12):  # for every x rotation
#     rad_in_x = (math.pi / 12) * i  # y axis rotation (in rads)
#     for j in range(12):  # for every y rotation
#         rad_in_y = (math.pi / 12) * j  # y axis rotation (in rads)
#         template_name = "/template{0}_{1}.mrc".format(i, j)
#         try:
#             template_cylinder = MapParser.readMRC(templates_dir + template_name)
#         except:
#             print Messages.ERROR_READING_TEMPLATE_FILE.format(template_name)
#
#         size = template_cylinder.box_size()
#         a = template_cylinder.apix
#         value = 0
#         for z in range(size[0]):
#             # print value
#             for y in range(size[1]):
#                 for x in range(size[2]):
#                     cX = (x - (size[2] // 2)) * a
#                     cY = (y - (size[1] // 2)) * a
#                     cZ = (z - (size[0] // 2)) * a
#
#                     template = template_cylinder.translate(cZ,cY,cX)
#                     try:
#                         # correlation_matrix = correlate(target_map.fullMap, template_cylinder.fullMap, mode="same")
#                         # correlation_matrix = norm_xcorr(template_cylinder.fullMap, target_map.fullMap)
#                         sF = ScoringFunctions()
#                         value = sF.CCC(target_map, template)
#                         if value > max_scores[x, y, z]:
#                             max_scores[x, y, z] = value
#                             max_dirs[x, y, z] = (rad_in_x, rad_in_y)
#                             print value
#
#                     except Exception as e:
#                         print e
#                         print Messages.CORRELATION_ERROR.format(template_name)
#
#
#
# print Messages.DONE_CORRELATION
# if debug:
#
#     dir_path = os.path.dirname(os.path.realpath(__file__))
#     if not os.path.exists(dir_path + corr_dir):
#         os.makedirs(dir_path + corr_dir)
#
#     score_file = open(dir_path + corr_dir + "/max_score", "w+")
#     dirs_file = open(dir_path + corr_dir + "/max_dirs", "w+")
#     np.save(score_file, max_scores)
#     np.save(dirs_file, max_dirs)
#     score_file.close()
#     dirs_file.close()
#
# return max_scores, max_dirs

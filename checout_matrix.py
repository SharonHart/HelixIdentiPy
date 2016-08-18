import os
import numpy as np
# corr_dir = "/correlation"
# out_file = file("." + corr_dir + "/above_thr.txt", "w+")
# dir_path = os.path.dirname(os.path.realpath(__file__))
#
# # score_file = file()
# # dirs_file = file()
# scores = np.load("." + corr_dir + "/max_score")
# directions = np.load("." + corr_dir + "/max_dirs")
# print scores.shape
# print scores.max()
# # print >>out_file, scores.max()
# counter = 0
# for i in range(scores.shape[0]):
#     for j in range(scores.shape[1]):
#         for k in range(scores.shape[2]):
#             # print scores[i,j,k]
#             if scores[i,j,k] >= 30:
#                 counter += 1
#                 print "Value: {}\tPoint: {}\tDirection: {}".format(scores[i,j,k], (i,j,k), directions[i,j,k]*57.2958)
#                 # print >>out_file, "Value: {}\tPoint: {}\tDirection: {}".format(scores[i,j,k], (i,j,k), directions[i,j,k]*57.2958)
# print counter
# # score_file.close()
# # dirs_file.close()
def checkitout():
    corr_dir = "/correlation"
    out_file = file("." + corr_dir + "/above_thr.txt", "w+")
    dir_path = os.path.dirname(os.path.realpath(__file__))

    # score_file = file()
    # dirs_file = file()
    scores = np.load("." + corr_dir + "/max_score")
    directions = np.load("." + corr_dir + "/max_dirs")
    print scores.shape
    print scores.max()
    # print >>out_file, scores.max()
    counter = 0
    for i in range(scores.shape[0]):
        for j in range(scores.shape[1]):
            for k in range(scores.shape[2]):
                # print scores[i,j,k]
                if scores[i,j,k] >= 30:
                    counter += 1
                    print "Value: {}\tPoint: {}\tDirection: {}".format(scores[i,j,k], (i,j,k), directions[i,j,k]*57.2958)
                    # print >>out_file, "Value: {}\tPoint: {}\tDirection: {}".format(scores[i,j,k], (i,j,k), directions[i,j,k]*57.2958)
    print counter
    # score_file.close()
    # dirs_file.close()
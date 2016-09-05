"""
Creates an ideal cylinder in a map file format.
"""

def main(target_map):

    # 2 Very very simple example of the cylinder
    dr = 2.3  # radius of the cylinder
    h = 10.8  # height of the cylinder
    rho = 1  # density of the cylinder

    target_map.shift_origin(0, 0, 0)

    dz = len(target_map.fullMap) * target_map.apix / 2
    dy = len(target_map.fullMap[0]) * target_map.apix / 2
    dx = len(target_map.fullMap[0][0]) * target_map.apix / 2

    for z in range(len(target_map.fullMap)):
        for y in range(len(target_map.fullMap[z])):
            for x in range(len(target_map.fullMap[z][y])):
                z_coor = z * target_map.apix - dz
                y_coor = y * target_map.apix - dy
                x_coor = x * target_map.apix - dx

                if (z_coor < h) & (z_coor > 0) & (y_coor * y_coor + x_coor * x_coor < dr * dr):
                    target_map.fullMap[z][y][x] = rho
                else:
                    target_map.fullMap[z][y][x] = 0

    return target_map

"""
Creates Ideal Cylinder based on the input map.
"""

def main(map_target):
    """
    :param map_target: Target map instance
    :return: Map instance representing an ideal cylinder
    """
    # Get the apix from the target map for cylinder parameters calculations
    apix = map_target.apix

    dr = 2.3/apix  # Ideal cylinder radius
    h = 10.8/apix  # Ideal cylinder height. Two turned Helix
    rho = 1  # Ideal cylinder density.

    map_target.shift_origin(0, 0, 0)

    dz = len(map_target.fullMap) * map_target.apix / 2
    dy = len(map_target.fullMap[0]) * map_target.apix / 2
    dx = len(map_target.fullMap[0][0]) * map_target.apix / 2

    for z in range(len(map_target.fullMap)):
        for y in range(len(map_target.fullMap[z])):
            for x in range(len(map_target.fullMap[z][y])):
                z_coor = z * map_target.apix - dz
                y_coor = y * map_target.apix - dy
                x_coor = x * map_target.apix - dx

                if (z_coor < h) & (z_coor > 0) & (y_coor * y_coor + x_coor * x_coor < dr * dr):
                    map_target.fullMap[z][y][x] = rho
                else:
                    map_target.fullMap[z][y][x] = 0

    return map_target

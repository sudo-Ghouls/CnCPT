# Author: Thomas C.F. Goolsby - tgoolsby@mit.edu
# This file was created in support of the CNCPT Thesis
# Fall 2020 - EM.THE


from random import randrange

from shapely.geometry import Point

from Simulation.GeographyPhysics.core import bearing, haversine

NOISE_BOUND = (-90, 90)


def patrol(unit):
    my_location = Point(unit.kinematics.get_location())
    dis_to_center = haversine(my_location, unit.area.center)
    if not unit.area.contains(my_location):
        if unit.area._length is not None and dis_to_center > unit.area._length:
            noise = 0
        else:
            noise = randrange(NOISE_BOUND[0], NOISE_BOUND[1])
        bearing_to_center = bearing(my_location, unit.area.center)

        bearing_to_center = bearing_to_center + noise
        unit.kinematics.set_heading(bearing_to_center)

# Author: Thomas C.F. Goolsby - tgoolsby@mit.edu
# This file was created in support of the CNCPT Thesis
# Fall 2020 - EM.THE


from random import randrange

from CnCPT.Simulation.GeographyPhysics import Geography
from shapely.geometry import Point
NOISE_BOUND = (-90, 90)


def patrol(unit):
    my_location = Point(unit.kinematics.get_location())
    if not unit.area.contains(my_location):
        bearing_to_center = Geography.bearing(my_location, unit.area.center)
        noise = randrange(NOISE_BOUND[0], NOISE_BOUND[1])
        # noise = 0
        bearing = bearing_to_center + noise
        unit.kinematics.set_heading(bearing)

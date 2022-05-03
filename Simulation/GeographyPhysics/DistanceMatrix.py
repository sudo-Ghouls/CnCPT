# Author: Thomas C.F. Goolsby - tgoolsby@mit.edu
# This file was created in support of the CNCPT Thesis
# Fall 2020 - EM.THE

import numpy as np
from scipy.spatial.distance import cdist

from Simulation.GeographyPhysics.core import haversine, bearing
from Simulation.Utility.SideEnum import SideEnum


class DistanceMatrix:
    def __init__(self, units):
        self.unit_map = {}
        self.distances = []
        self.bearings = []
        self.update(units)

    def update(self, units):
        blue_active_units = [unit for unit in units if unit.side is SideEnum.BLUE and not unit.docked]
        red_active_units = [unit for unit in units if unit.side is SideEnum.RED and not unit.docked]
        self.blue_unit_map = {k.name: v for v, k in enumerate(blue_active_units)}
        self.red_unit_map = {k.name: v for v, k in enumerate(red_active_units)}
        blue_unit_locs = np.array([unit.kinematics.get_location() for unit in blue_active_units])
        red_unit_locs = np.array([unit.kinematics.get_location() for unit in red_active_units])
        self.distances = cdist(blue_unit_locs, red_unit_locs, metric=haversine)  # in meters
        self.bearings = cdist(blue_unit_locs, red_unit_locs, metric=bearing)

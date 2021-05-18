# Author: Thomas C.F. Goolsby - tgoolsby@mit.edu
# This file was created in support of the CNCPT Thesis
# Fall 2020 - EM.THE

import random

import numpy as np
from shapely.geometry import Polygon, Point

from CnCPT.Simulation.GeographyPhysics import Geography


class Area(Polygon):
    def __init__(self, bounds):
        super(Area, self).__init__(shell=bounds)
        self.center = self.lat_lon_average()

    def lat_lon_average(self):
        lat_avg = np.mean([loc for loc in self.bounds[::2]])
        lon_avg = np.mean([loc for loc in self.bounds[1::2]])
        return lat_avg, lon_avg

    @staticmethod
    def create_patrol_area_from_center(center, length, width, unit='m'):
        half_w = length / 2.0
        half_l = width / 2.0
        top_center = Geography.reckon(half_w, 0, center[0], center[1], unit=unit)
        top_left = Geography.reckon(half_l, 270, top_center[0], top_center[1], unit=unit)
        top_right = Geography.reckon(half_l, 90, top_center[0], top_center[1], unit=unit)
        bot_center = Geography.reckon(half_w, 180, center[0], center[1], unit=unit)
        bot_left = Geography.reckon(half_l, 270, bot_center[0], bot_center[1], unit=unit)
        bot_right = Geography.reckon(half_l, 90, bot_center[0], bot_center[1], unit=unit)
        bounds = (top_left, top_right, bot_left, bot_right)
        return Area(bounds)

    def random_starting_loc_in_poly(self):
        """ This method generates a point inside the shapely Polygon object passed in. If you wish to have a more
        restrictive point generation (i.e. prevent a unit from starting on land or water), subclass and override this
        method

        :param self: shapely Polygon object
        :return: shapely POINT object
        """
        minx, miny, maxx, maxy = self.bounds
        while True:
            location = Point(random.uniform(minx, maxx), random.uniform(miny, maxy))
            if self.contains(location):
                return location
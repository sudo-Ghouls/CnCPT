# Author: Thomas C.F. Goolsby - tgoolsby@mit.edu
# This file was created in support of the CNCPT Thesis
# Fall 2020 - EM.THE

import numpy as np


class Kinematics:
    def __init__(self):
        """

        """
        self._location = [0.0, 0.0]  # lat, lon in deg
        self._heading = 0.0  # degrees
        self._speed = 0.0  # m/s
        self._max_speed = 0.0  # m/s
        self._max_range = 0  # m
        self._range_travelled = 0  # m

    def set_location(self, lat=None, lon=None, unit=None):
        """

        :param x:
        :param y:
        """
        if unit is not None:
            self._location[0], self._location[1] = unit.kinematics.get_location()

        if lat is not None and lon is not None:
            self._location[0] = lat
            self._location[1] = lon

    def get_location(self):
        """

        :return:
        """
        return self._location

    def get_location_radians(self):
        """

        :return:
        """
        return [np.radians(self._location[0]), np.radians(self._location[1])]

    def set_heading(self, heading=None):
        """

        :param heading:
        :return:
        """
        if heading is not None:
            self._heading = heading

    def get_heading(self):
        """

        :return:
        """
        return self._heading

    def get_heading_radians(self):
        """

        :return:
        """
        return np.radians(self._heading)

    def set_speed(self, speed=None):
        """

        :param speed:
        :return:
        """
        if speed is not None:
            self._speed = speed

    def get_speed(self):
        """

        :return:
        """
        return self._speed

    def set_max_speed(self, max_speed=None):
        """

        :param max_speed:
        :return:
        """
        if max_speed is not None:
            self._max_speed = max_speed

    def get_max_speed(self):
        """

        :return:
        """
        return self._max_speed

    def set_max_range(self, max_range=None):
        """

        :param max_range:
        :return:
        """
        if max_range is not None:
            self._max_range = max_range

    def get_max_range(self):
        """

        :return:
        """
        return self._max_range

    def update_range_traveled(self, range_traveled):
        """

        :param range_traveled:
        :return:
        """
        self._range_travelled += range_traveled

    def get_range_traveled(self):
        """

        :return:
        """
        return self._range_travelled

    def reset_range_traveled(self):
        """

        :return:
        """
        self._range_travelled = 0

    def initialize(self, name, **kwargs):
        """

        :param name: unit name; used to provide user awareness of problematics initializations
        :param kwargs:
        :return:
        """

        location = kwargs.pop('location', None)
        if location is not None:
            location = np.array(location)
            x, y = location
        else:
            x = kwargs.pop('x', None)
            y = kwargs.pop('y', None)
            if x is None or y is None:
                raise ("Unit '{0}' Kinematics have no location information".format(name))
        heading = kwargs.pop("heading", None)
        speed = kwargs.pop("speed", None)
        max_speed = kwargs.pop("max_speed", None)

        # Set Kinematics
        self.set_location(x, y)
        self.set_heading(heading)
        self.set_speed(speed)
        self.set_max_speed(max_speed)

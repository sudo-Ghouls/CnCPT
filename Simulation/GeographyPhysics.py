# Author: Thomas C.F. Goolsby - tgoolsby@mit.edu
# This file was created in support of the CNCPT Thesis
# Fall 2020 - EM.THE

import numpy as np
from scipy.spatial.distance import cdist
from shapely.geometry import Polygon, Point

from CnCPT.Simulation.Units.State import State
from CnCPT.Simulation.Utility.SideEnum import SideEnum

earth_radius = 6378.1  # km
# Unit values taken from http://www.unitconversion.org/unit_converter/length.html
_CONVERSIONS = {"km": 1.0,
                "m": 1000.0,
                "mi": 0.621371192,
                "nmi": 0.539956803,
                "ft": 3280.839895013,
                "in": 39370.078740158}


def wrapto360(angle):
    return (angle + 360) % 360


def bearing_change(ang1, ang2):
    ang1 = wrapto360(ang1)
    ang2 = wrapto360(ang2)
    max_ang = max((ang1, ang2))
    min_ang = min((ang1, ang2))
    return wrapto360(max_ang - min_ang)


class Geography:
    def __init__(self, all_units, new_bounds):
        self.description = "2-D Spherical Earth using meters for distance and degrees for angle"
        if new_bounds is not None:
            self.update_map(new_bounds)
        else:
            self.map = None
        self.distance_matrix = DistanceMatrix(all_units)

    def update(self, units):
        self.distance_matrix.update(units)

    @staticmethod
    def propagate(unit, timestep):
        """
        Propagates unit if it is not part of a group. If it is part of a group teleport to proper position in formation
        :param unit:
        :param timestep:
        :return:
        """

        if unit.leader is not None and unit.formation_lock is True:
            leader_location = unit.leader.kinematics.get_location()
            leader_heading = unit.leader.kinematics.get_heading()
            new_lat, new_lon = Geography.reckon(unit.my_range_from_leader, unit.my_bearing_from_leader,
                                                leader_location[0], leader_location[1])
            unit.kinematics.set_location(lat=new_lat, lon=new_lon)
            unit.kinematics.set_heading(leader_heading)
        elif unit.route_propagation is True:
            unit.route.propagate_on_route(unit, timestep)
        else:
            d = unit.kinematics.get_speed() * timestep  # m/s * s
            bearing = unit.kinematics.get_heading()
            current_lat = unit.kinematics.get_location()[0]
            current_lon = unit.kinematics.get_location()[1]
            new_lat, new_lon = Geography.reckon(d, bearing, current_lat, current_lon)
            unit.kinematics.set_location(lat=new_lat, lon=new_lon)

    @staticmethod
    def reckon(distance, bearing, lat, lon, unit='m'):
        # handle conversions
        e = earth_radius * _CONVERSIONS[unit]

        # convert all latitudes/longitudes to radians
        lat, lon = np.radians(lat), np.radians(lon)
        bearing = np.radians(wrapto360(bearing))

        # do math
        arc = distance / e
        new_lat = np.arcsin(np.sin(lat) * np.cos(arc) +
                            np.cos(lat) * np.sin(arc) * np.cos(bearing))

        lon += np.arctan2(np.sin(bearing) * np.sin(arc),
                          np.cos(lat) * np.cos(arc) -
                          np.sin(lat) * np.sin(arc) * np.cos(bearing))
        new_lat = np.degrees(new_lat)
        new_lon = np.degrees(lon)
        return new_lat, new_lon

    def update_map(self, new_bounds):
        self.map = Polygon(new_bounds)

    def distance_between_units(self, unit_a, unit_b):
        return self.distance_matrix.distances[self.distance_matrix.unit_map[unit_a.name]][
            self.distance_matrix.unit_map[unit_b.name]]

    def targets_in_range(self, unit, max_range):
        if unit.side is SideEnum.BLUE:
            my_unit_map = self.distance_matrix.blue_unit_map
            enemy_unit_map = self.distance_matrix.red_unit_map
            my_unit = my_unit_map[unit.name]
            my_distance_matrix = self.distance_matrix
            data = [(i, j) for (i, j) in zip(my_distance_matrix.distances[my_unit, :], enemy_unit_map) if
                    i <= max_range]
            return [val[1] for val in data], [val[0] for val in data]
        elif unit.side is SideEnum.RED:
            my_unit_map = self.distance_matrix.red_unit_map
            enemy_unit_map = self.distance_matrix.blue_unit_map
            my_unit = my_unit_map[unit.name]
            my_distance_matrix = self.distance_matrix
            data = [(i, j) for (i, j) in zip(my_distance_matrix.distances[:, my_unit], enemy_unit_map) if
                    i <= max_range]
            return [val[1] for val in data], [val[0] for val in data]
        else:
            raise Exception("GeographyPhysics.py : Distances for Sides Other that Red and Blue not Currently Enabled")

    @staticmethod
    def haversine(point1, point2, unit='m'):
        # convert all latitudes/longitudes to radians
        if isinstance(point1, Point):
            lat1, lon1 = np.radians(point1.coords[0][0]), np.radians(point1.coords[0][1])
        else:
            lat1, lon1 = np.radians(point1[0]), np.radians(point1[1])
        if isinstance(point2, Point):
            lat2, lon2 = np.radians(point2.coords[0][0]), np.radians(point2.coords[0][1])
        else:
            lat2, lon2 = np.radians(point2[0]), np.radians(point2[1])

        # calculate haversine
        lat = lat2 - lat1
        lon = lon2 - lon1
        d = np.sin(lat * 0.5) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(lon * 0.5) ** 2
        return 2 * earth_radius * _CONVERSIONS[unit] * np.arcsin(np.sqrt(d))

    @staticmethod
    def bearing(point1, point2):
        # convert all latitudes/longitudes to radians
        if isinstance(point1, Point):
            lat1, lon1 = np.radians(point1.coords[0][0]), np.radians(point1.coords[0][1])
        else:
            lat1, lon1 = np.radians(point1[0]), np.radians(point1[1])
        if isinstance(point2, Point):
            lat2, lon2 = np.radians(point2.coords[0][0]), np.radians(point2.coords[0][1])
        else:
            lat2, lon2 = np.radians(point2[0]), np.radians(point2[1])
        # calculate bearing
        dlon = lon2 - lon1
        ang_rad = np.arctan2(np.sin(dlon) * np.cos(lat2), np.cos(lat1) * np.sin(lat2) - np.sin(
            lat1) * np.cos(lat2) * np.cos(dlon))
        ang_deg = np.degrees(ang_rad)

        return ang_deg


class DistanceMatrix:
    def __init__(self, units):
        self.unit_map = {}
        self.distances = []
        self.bearings = []
        self.update(units)

    def update(self, units):
        blue_active_units = [unit for unit in units if unit.side is SideEnum.BLUE and unit.state is not State.DOCKED]
        red_active_units = [unit for unit in units if unit.side is SideEnum.RED and unit.state is not State.DOCKED]
        self.blue_unit_map = {k.name: v for v, k in enumerate(blue_active_units)}
        self.red_unit_map = {k.name: v for v, k in enumerate(red_active_units)}
        blue_unit_locs = np.array([unit.kinematics.get_location() for unit in blue_active_units])
        red_unit_locs = np.array([unit.kinematics.get_location() for unit in red_active_units])
        self.distances = cdist(blue_unit_locs, red_unit_locs, metric=Geography.haversine)  # in meters
        self.bearings = cdist(blue_unit_locs, red_unit_locs, metric=Geography.bearing)


class Route:
    def __init__(self, waypoints):
        self.waypoints = waypoints
        self.idx = 1
        self.direction = 0  # 0 is nominal, 1 is reversed
        self.last_dis = 0
        self.last_bear = None

    def _get_next_waypoint(self):
        if self.idx == 0 and self.direction:
            self.direction = 0
        elif self.idx == len(self.waypoints) - 1 and not self.direction:
            self.direction = 1
        if not self.direction:
            self.idx = self.idx + 1
            return self.waypoints[self.idx]
        else:
            self.idx = self.idx - 1
            return self.waypoints[self.idx]

    def propagate_on_route(self, unit, time_step):
        unit_loc = unit.kinematics.get_location()
        unit_distance_traveled = unit.kinematics.get_speed() * time_step
        distance_to_travel = unit_distance_traveled
        waypoint = unit.route.waypoints[unit.route.idx]
        dist_to_waypoint, bear_to_waypoint = Geography.haversine(unit_loc, waypoint), \
                                             Geography.bearing(unit_loc, waypoint)
        if dist_to_waypoint <= distance_to_travel:
            next_waypoint = self._get_next_waypoint()
            bear_to_next_waypoint = Geography.bearing(waypoint, next_waypoint)
            distance_to_travel -= dist_to_waypoint
            new_lat, new_lon = Geography.reckon(distance_to_travel, bear_to_next_waypoint, waypoint[0], waypoint[1])
            unit.kinematics.set_location(lat=new_lat, lon=new_lon)
            unit.kinematics.set_heading(bear_to_waypoint)
        else:
            new_lat, new_lon = Geography.reckon(distance_to_travel, bear_to_waypoint, unit_loc[0], unit_loc[1])
            unit.kinematics.set_location(lat=new_lat, lon=new_lon)
            unit.kinematics.set_heading(bear_to_waypoint)


class Kinematics:
    def __init__(self):
        """

        """
        self._location = [0.0, 0.0]  # lat, lon in deg
        self._heading = 0.0  # degrees
        self._speed = 0.0  # m/s
        self._max_speed = 0.0  # m/s

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

# Author: Thomas C.F. Goolsby - tgoolsby@mit.edu
# This file was created in support of the CNCPT Thesis
# Fall 2020 - EM.THE

import numpy as np
from shapely.geometry import Polygon

from Simulation.GeographyPhysics.DistanceMatrix import DistanceMatrix
from Simulation.GeographyPhysics.core import earth_radius, _CONVERSIONS, wrapto360, haversine
from Simulation.Utility.SideEnum import SideEnum


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
        current_lat, current_lon = unit.kinematics.get_location()
        if unit.leader is not None and unit.formation_lock is True:
            leader_location = unit.leader.kinematics.get_location()
            leader_heading = unit.leader.kinematics.get_heading()
            new_lat, new_lon = Geography.reckon(unit.my_range_from_leader, unit.my_bearing_from_leader,
                                                leader_location[0], leader_location[1])

            d = haversine((new_lat, new_lon), (current_lat, current_lon))
            unit.kinematics.set_location(lat=new_lat, lon=new_lon)
            unit.kinematics.set_heading(leader_heading)
        elif unit.route_propagation is True:
            d = unit.route.propagate_on_route(unit, timestep)
        else:
            d = unit.kinematics.get_speed() * timestep  # m/s * s
            bearing = unit.kinematics.get_heading()
            new_lat, new_lon = Geography.reckon(d, bearing, current_lat, current_lon)
            unit.kinematics.set_location(lat=new_lat, lon=new_lon)
        return d

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
            raise Exception("Geography & Physics : Distances for Sides Other that Red and Blue not Currently Enabled")

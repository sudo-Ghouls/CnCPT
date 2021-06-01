# Author: Thomas C.F. Goolsby - tgoolsby@mit.edu
# This file was created in support of the CNCPT Thesis
# Fall 2020 - EM.THE

import math

from Simulation.GeographyPhysics import Geography, Route


class UnitGroup:
    def __init__(self, name, units, leader, route):
        """

        :param leader:
        :param route:
        :param units:
        """
        self.name = name
        self.leader = leader
        self.route = route
        self.units = units

    @staticmethod
    def construct_unit_group(name, units, leader=None, route=None):
        """

        :param name:
        :param units:
        :param leader:
        :param route:
        :return:
        """
        NewGroup = UnitGroup(name, units, leader, route)
        for unit in units:
            unit.group = NewGroup
            if unit is not leader:
                unit.leader = leader
                starting_bearing = Geography.bearing(route[0], route[1])
                unit.kinematics.set_heading(starting_bearing)
            else:
                unit.route = Route(route)
                unit.route_propagation = True
                unit.follower.append(unit)
                unit.kinematics.set_location(lat=route[0][0], lon=route[0][1])
                starting_bearing = Geography.bearing(route[0], route[1])
                unit.kinematics.set_heading(starting_bearing)
        UnitGroup.basic_formation(units)
        return NewGroup.units

    @staticmethod
    def basic_formation(units, angle_seperation_deg=90, range_seperation_m=1852):
        units_per_loop = math.floor(360.0 / angle_seperation_deg)
        center = units[0].kinematics.get_location()
        for idx, unit in enumerate(units):
            if idx == 0:
                continue
            loop, loopIdx = divmod(idx, units_per_loop)
            if loop == 0:
                dist_to_reckon = range_seperation_m
            else:
                dist_to_reckon = loop * range_seperation_m
            new_lat, new_lon = Geography.reckon(dist_to_reckon, angle_seperation_deg * loopIdx, center[0], center[1])
            unit.kinematics.set_location(new_lat, new_lon)
            unit.my_range_from_leader = dist_to_reckon
            unit.my_bearing_from_leader = angle_seperation_deg * loopIdx
            unit.formation_lock = True

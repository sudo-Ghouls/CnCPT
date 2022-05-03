# Author: Thomas C.F. Goolsby - tgoolsby@mit.edu
# This file was created in support of the CNCPT Thesis
# Fall 2020 - EM.THE

from shapely.geometry import Polygon

from Simulation.GeographyPhysics.DistanceMatrix import DistanceMatrix
from Simulation.GeographyPhysics.core import haversine, reckon
from Simulation.Utility.SideEnum import SideEnum


def propagate(simulation_manager):
    """
    This function propagates all units forward in time based on their current velocity and heading
    :return:
    """
    if len(simulation_manager.all_units) == 0:
        return
    units_to_propagate = simulation_manager.unit_filter.filter(alive=True, moving=True, docked=False)

    for unit in units_to_propagate:
        distance_propagated = Geography.propagate(unit, simulation_manager.time_step)
        unit.kinematics.update_range_traveled(distance_propagated)
    # list(map(Geography.propagate, units_to_propagate, itertools.repeat(simulation_manager.time_step, len(units_to_propagate))))

    units_currently_docked = simulation_manager.unit_filter.filter(alive=True, docked=True)
    for unit in units_currently_docked:
        if unit.parent is not None:
            if unit.docked is True:
                unit.kinematics.set_location(unit=unit.parent)
            else:
                unit.docked = False


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
            new_lat, new_lon = reckon(unit.my_range_from_leader, unit.my_bearing_from_leader,
                                      leader_location[0], leader_location[1])

            d = haversine((new_lat, new_lon), (current_lat, current_lon))
            unit.kinematics.set_location(lat=new_lat, lon=new_lon)
            unit.kinematics.set_heading(leader_heading)
        elif unit.route_propagation is True:
            d = unit.route.propagate_on_route(unit, timestep)
        else:
            d = unit.kinematics.get_speed() * timestep  # m/s * s
            bearing = unit.kinematics.get_heading()
            new_lat, new_lon = reckon(d, bearing, current_lat, current_lon)
            unit.kinematics.set_location(lat=new_lat, lon=new_lon)
        return d

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

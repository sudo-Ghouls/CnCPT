# Author: Thomas C.F. Goolsby - tgoolsby@mit.edu
# This file was created in support of the CNCPT Thesis
# Fall 2020 - EM.THE

from Simulation.Units.BaseClasses.Ship import Ship
from Simulation.Units.core import BasicBehavior
from Simulation.Utility.SideEnum import SideEnum


class Gunboat(Ship):
    def __init__(self, name=None, behavior=None, location=None, spawn_polygon=None, side=SideEnum.RED, route=None,
                 parent=None, network=None, group_data=None, kinematics_data=None):
        super().__init__(name=name, behavior=behavior, location=location, spawn_polygon=spawn_polygon,
                         side=side, route=route, parent=parent, network=network, group_data=group_data,
                         kinematics_data=kinematics_data)
        self.my_type = "Gunboat"
        self.cost = 50

    @staticmethod
    def behavior_aggressive(unit, simulation_manager):
        pass

    @staticmethod
    def behavior_passive(unit, simulation_manager):
        pass

    @staticmethod
    def behavior_baseline(unit, simulation_manager):
        unit.kinematics.set_speed(10)
        BasicBehavior.RouteFollowing(unit, simulation_manager)


class KeijoMaru(Gunboat):
    def __init__(self, name="KeijoMaru", behavior=Gunboat.behavior_baseline, location=None, spawn_polygon=None,
                 side=SideEnum.RED, route=None, parent=None, network=None, group_data=None, kinematics_data=None):
        super().__init__(name=name, behavior=behavior, location=location, spawn_polygon=spawn_polygon,
                         side=side, route=route, parent=parent, network=network, group_data=group_data,
                         kinematics_data=kinematics_data)


class SeikaiMaru(Gunboat):
    def __init__(self, name="SeikaiMaru", behavior=Gunboat.behavior_baseline, location=None, spawn_polygon=None,
                 side=SideEnum.RED, route=None, parent=None, network=None, group_data=None, kinematics_data=None):
        super().__init__(name=name, behavior=behavior, location=location, spawn_polygon=spawn_polygon,
                         side=side, route=route, parent=parent, network=network, group_data=group_data,
                         kinematics_data=kinematics_data)


class NikkaiMaru(Gunboat):
    def __init__(self, name="NikkaiMaru", behavior=Gunboat.behavior_baseline, location=None, spawn_polygon=None,
                 side=SideEnum.RED, route=None, parent=None, network=None, group_data=None, kinematics_data=None):
        super().__init__(name=name, behavior=behavior, location=location, spawn_polygon=spawn_polygon,
                         side=side, route=route, parent=parent, network=network, group_data=group_data,
                         kinematics_data=kinematics_data)

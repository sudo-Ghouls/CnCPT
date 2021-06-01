# Author: Thomas C.F. Goolsby - tgoolsby@mit.edu
# This file was created in support of the CNCPT Thesis
# Fall 2020 - EM.THE

from Input.CoralSea.BaseClasses.Ship import Ship
from Simulation.Units.core import BasicBehavior
from Simulation.Utility.SideEnum import SideEnum


class Tanker(Ship):
    def __init__(self, name=None, behavior=None, location=None, spawn_polygon=None):
        super().__init__(name=name, behavior=behavior, location=location, spawn_polygon=spawn_polygon,
                         side=SideEnum.RED)
        self.cost = 200

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


class TohoMaru(Tanker):
    def __init__(self, name="TohoMaru", behavior=Tanker.behavior_baseline, location=None, spawn_polygon=None):
        super().__init__(name, behavior, location, spawn_polygon)

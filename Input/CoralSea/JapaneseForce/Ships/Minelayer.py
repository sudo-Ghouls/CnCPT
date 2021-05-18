# Author: Thomas C.F. Goolsby - tgoolsby@mit.edu
# This file was created in support of the CNCPT Thesis
# Fall 2020 - EM.THE

from CnCPT.Input.CoralSea.BaseClasses.Ship import Ship
from CnCPT.Simulation.UnitBehavior import BasicBehavior
from CnCPT.Simulation.Utility.SideEnum import SideEnum


class Minelayer(Ship):
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


class Tsugaru(Minelayer):
    def __init__(self, name="Tsugaru", behavior=Minelayer.behavior_baseline, location=None, spawn_polygon=None):
        super().__init__(name, behavior, location, spawn_polygon)


class Okinoshima(Minelayer):
    def __init__(self, name="Okinoshima", behavior=Minelayer.behavior_baseline, location=None, spawn_polygon=None):
        super().__init__(name, behavior, location, spawn_polygon)


class KoeiMaru(Minelayer):
    def __init__(self, name="KoeiMaru", behavior=Minelayer.behavior_baseline, location=None, spawn_polygon=None):
        super().__init__(name, behavior, location, spawn_polygon)

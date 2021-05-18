# Author: Thomas C.F. Goolsby - tgoolsby@mit.edu
# This file was created in support of the CNCPT Thesis
# Fall 2020 - EM.THE

from CnCPT.Input.CoralSea.BaseClasses.Aircraft import Aircraft
from CnCPT.Simulation.Utility.SideEnum import SideEnum


class Fighter(Aircraft):
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
        pass


class A6M2Zero(Fighter):
    def __init__(self, name="A6M2Zero", behavior=Fighter.behavior_baseline, location=None, spawn_polygon=None):
        super().__init__(name, behavior, location, spawn_polygon)


class MitsubishiA5MType96(Fighter):
    def __init__(self, name="MitsubishiA5MType96", behavior=Fighter.behavior_baseline, location=None,
                 spawn_polygon=None):
        super().__init__(name, behavior, location, spawn_polygon)

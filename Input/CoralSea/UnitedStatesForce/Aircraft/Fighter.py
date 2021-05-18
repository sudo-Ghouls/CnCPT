# Author: Thomas C.F. Goolsby - tgoolsby@mit.edu
# This file was created in support of the CNCPT Thesis
# Fall 2020 - EM.THE

from CnCPT.Input.CoralSea.BaseClasses.Aircraft import Aircraft
from CnCPT.Input.CoralSea.UnitedStatesForce.Sensors.Visual import VisualAir
from CnCPT.Input.CoralSea.UnitedStatesForce.Weapons.air_to_air import AirToAirGun
from CnCPT.Simulation.Logic.Patrol import patrol
from CnCPT.Simulation.Units.State import State
from CnCPT.Simulation.Utility.SideEnum import SideEnum


class Fighter(Aircraft):
    def __init__(self, name=None, behavior=None, location=None, spawn_polygon=None):
        super().__init__(name=name, behavior=behavior, location=location, spawn_polygon=spawn_polygon,
                         side=SideEnum.BLUE)
        self.cost = 200
        self.add_sensor(VisualAir())
        self.add_weapon(AirToAirGun, 100)
        if behavior is None:
            self.my_brain = self.behavior_baseline

    @staticmethod
    def behavior_baseline(unit, simulation_manager):
        if unit.state is State.SEARCH:
            patrol(unit)

    @staticmethod
    def behavior_aggressive(unit, simulation_manager):
        pass

    @staticmethod
    def behavior_passive(unit, simulation_manager):
        pass


class GrummanF4F3Wildcat(Fighter):
    def __init__(self, name="GrummanF4F3Wildcat", behavior=None, location=None, spawn_polygon=None):
        super().__init__(name, behavior, location, spawn_polygon)
        self.kinematics.set_max_speed(288)  # Max speed from https://en.wikipedia.org/wiki/Grumman_F4F_Wildcat

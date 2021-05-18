# Author: Thomas C.F. Goolsby - tgoolsby@mit.edu
# This file was created in support of the CNCPT Thesis
# Fall 2020 - EM.THE

from CnCPT.Input.CoralSea.BaseClasses.Aircraft import Aircraft
from CnCPT.Input.CoralSea.UnitedStatesForce.Sensors.Visual import VisualAir
from CnCPT.Input.CoralSea.UnitedStatesForce.Weapons.air_to_surface import AirLaunchedBomb
from CnCPT.Simulation.Logic.General import determine_priority_target_contact, pursue_target
from CnCPT.Simulation.Logic.Patrol import patrol
from CnCPT.Simulation.Units.State import State
from CnCPT.Simulation.Utility.SideEnum import SideEnum


class DiveBomber(Aircraft):
    def __init__(self, name=None, behavior=None, location=None, spawn_polygon=None):
        super().__init__(name=name, behavior=behavior, location=location, spawn_polygon=spawn_polygon,
                         side=SideEnum.BLUE)
        self.cost = 200
        self.add_sensor(VisualAir())
        self.add_weapon(AirLaunchedBomb, 2)
        if behavior is None:
            self.my_brain = self.behavior_baseline

    @staticmethod
    def behavior_baseline(unit, simulation_manager):
        if unit.state is State.SEARCH:
            if bool(unit.contacts) and unit.target is None:
                target_contact = determine_priority_target_contact(unit.contacts, method='range')
                unit.target = target_contact.target_name_truth
            if unit.target:
                target_contact = unit.contacts[unit.target]
                pursue_target(unit, target_contact,standoff_range_m=50000)
            else:
                patrol(unit)

    @staticmethod
    def behavior_aggressive(unit, simulation_manager):
        pass

    @staticmethod
    def behavior_passive(unit, simulation_manager):
        pass


class DouglasSBDDauntless(DiveBomber):
    def __init__(self, name="DouglasSBDDauntless", behavior=None, location=None, spawn_polygon=None):
        super().__init__(name, behavior, location, spawn_polygon)
        self.kinematics.set_max_speed(161)  # Cruise speed from https://en.wikipedia.org/wiki/Douglas_SBD_Dauntless

# Author: Thomas C.F. Goolsby - tgoolsby@mit.edu
# This file was created in support of the CNCPT Thesis
# Fall 2020 - EM.THE

from Input.CoralSea.BaseClasses.Ship import Ship
from Input.CoralSea.UnitedStatesForce.Sensors.Visual import VisualSurface
from Input.CoralSea.UnitedStatesForce.Weapons.deck_gun import DeckGunAir
from Simulation.Utility.Conversions import kts_to_ms
from Simulation.Utility.SideEnum import SideEnum


class Oiler(Ship):
    def __init__(self, name=None, behavior=None, location=None, spawn_polygon=None):
        super().__init__(name=name, behavior=behavior, location=location, spawn_polygon=spawn_polygon,
                         side=SideEnum.BLUE)
        self.cost = 200
        self.add_sensor(VisualSurface())
        self.add_weapon(DeckGunAir, 1000)

    @staticmethod
    def behavior_aggressive(unit, simulation_manager):
        pass

    @staticmethod
    def behavior_passive(unit, simulation_manager):
        pass

    @staticmethod
    def behavior_baseline(unit, simulation_manager):
        unit.kinematics.set_speed(kts_to_ms(20))


class Neosho(Oiler):
    def __init__(self, name="Neosho", behavior=Oiler.behavior_baseline, location=None, spawn_polygon=None):
        super().__init__(name, behavior, location, spawn_polygon)


class Tippecanoe(Oiler):
    def __init__(self, name="Tippecanoe", behavior=Oiler.behavior_baseline, location=None, spawn_polygon=None):
        super().__init__(name, behavior, location, spawn_polygon)

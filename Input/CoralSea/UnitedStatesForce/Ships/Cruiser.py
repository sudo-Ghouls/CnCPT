# Author: Thomas C.F. Goolsby - tgoolsby@mit.edu
# This file was created in support of the CNCPT Thesis
# Fall 2020 - EM.THE

from CnCPT.Input.CoralSea.BaseClasses.Ship import Ship
from CnCPT.Input.CoralSea.UnitedStatesForce.Sensors.Visual import VisualSurface
from CnCPT.Input.CoralSea.UnitedStatesForce.Weapons.deck_gun import DeckGunAir, DeckGunSurface
from CnCPT.Simulation.Utility.Conversions import kts_to_ms
from CnCPT.Simulation.Utility.SideEnum import SideEnum


class Cruiser(Ship):
    def __init__(self, name=None, behavior=None, location=None, spawn_polygon=None):
        super().__init__(name=name, behavior=behavior, location=location, spawn_polygon=spawn_polygon,
                         side=SideEnum.BLUE)
        self.cost = 200
        self.add_sensor(VisualSurface())
        self.add_weapon(DeckGunAir, 1000)
        self.add_weapon(DeckGunSurface, 1000)

    @staticmethod
    def behavior_aggressive(unit, simulation_manager):
        pass

    @staticmethod
    def behavior_passive(unit, simulation_manager):
        pass

    @staticmethod
    def behavior_baseline(unit, simulation_manager):
        unit.kinematics.set_speed(kts_to_ms(20))


class AustralianCruiser(Cruiser):
    def __init__(self, name=None, behavior=None, location=None, spawn_polygon=None):
        super().__init__(name=name, behavior=behavior, location=location, spawn_polygon=spawn_polygon)
        self.cost = 200

    @staticmethod
    def behavior_aggressive(unit, simulation_manager):
        pass

    @staticmethod
    def behavior_passive(unit, simulation_manager):
        pass


class Minneapolis(Cruiser):
    def __init__(self, name="Minneapolis", behavior=Cruiser.behavior_baseline, location=None, spawn_polygon=None):
        super().__init__(name, behavior, location, spawn_polygon)


class NewOrleans(Cruiser):
    def __init__(self, name="NewOrleans", behavior=Cruiser.behavior_baseline, location=None, spawn_polygon=None):
        super().__init__(name, behavior, location, spawn_polygon)


class Astoria(Cruiser):
    def __init__(self, name="Astoria", behavior=Cruiser.behavior_baseline, location=None, spawn_polygon=None):
        super().__init__(name, behavior, location, spawn_polygon)


class Chester(Cruiser):
    def __init__(self, name="Chester", behavior=Cruiser.behavior_baseline, location=None, spawn_polygon=None):
        super().__init__(name, behavior, location, spawn_polygon)


class Portland(Cruiser):
    def __init__(self, name="Portland", behavior=Cruiser.behavior_baseline, location=None, spawn_polygon=None):
        super().__init__(name, behavior, location, spawn_polygon)


class Chicago(Cruiser):
    def __init__(self, name="Chicago", behavior=Cruiser.behavior_baseline, location=None, spawn_polygon=None):
        super().__init__(name, behavior, location, spawn_polygon)


class Australia(AustralianCruiser):
    def __init__(self, name="Australia", behavior=Cruiser.behavior_baseline, location=None, spawn_polygon=None):
        super().__init__(name, behavior, location, spawn_polygon)


class Hobart(AustralianCruiser):
    def __init__(self, name="Hobart", behavior=Cruiser.behavior_baseline, location=None, spawn_polygon=None):
        super().__init__(name, behavior, location, spawn_polygon)

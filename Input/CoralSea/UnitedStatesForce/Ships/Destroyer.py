# Author: Thomas C.F. Goolsby - tgoolsby@mit.edu
# This file was created in support of the CNCPT Thesis
# Fall 2020 - EM.THE

from CnCPT.Input.CoralSea.BaseClasses.Ship import Ship
from CnCPT.Input.CoralSea.UnitedStatesForce.Sensors.Visual import VisualSurface
from CnCPT.Input.CoralSea.UnitedStatesForce.Weapons.deck_gun import DeckGunAir, DeckGunSurface
from CnCPT.Simulation.Utility.Conversions import kts_to_ms
from CnCPT.Simulation.Utility.SideEnum import SideEnum


class Destroyer(Ship):
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


class Phelps(Destroyer):
    def __init__(self, name="Phelps", behavior=Destroyer.behavior_baseline, location=None, spawn_polygon=None):
        super().__init__(name, behavior, location, spawn_polygon)


class Dewey(Destroyer):
    def __init__(self, name="Dewey", behavior=Destroyer.behavior_baseline, location=None, spawn_polygon=None):
        super().__init__(name, behavior, location, spawn_polygon)


class Farragut(Destroyer):
    def __init__(self, name="Farragut", behavior=Destroyer.behavior_baseline, location=None, spawn_polygon=None):
        super().__init__(name, behavior, location, spawn_polygon)


class Alywin(Destroyer):
    def __init__(self, name="Alywin", behavior=Destroyer.behavior_baseline, location=None, spawn_polygon=None):
        super().__init__(name, behavior, location, spawn_polygon)


class Monaghan(Destroyer):
    def __init__(self, name="Monaghan", behavior=Destroyer.behavior_baseline, location=None, spawn_polygon=None):
        super().__init__(name, behavior, location, spawn_polygon)


class Morris(Destroyer):
    def __init__(self, name="Morris", behavior=Destroyer.behavior_baseline, location=None, spawn_polygon=None):
        super().__init__(name, behavior, location, spawn_polygon)


class Anderson(Destroyer):
    def __init__(self, name="Anderson", behavior=Destroyer.behavior_baseline, location=None, spawn_polygon=None):
        super().__init__(name, behavior, location, spawn_polygon)


class Hammann(Destroyer):
    def __init__(self, name="Hammann", behavior=Destroyer.behavior_baseline, location=None, spawn_polygon=None):
        super().__init__(name, behavior, location, spawn_polygon)


class Russell(Destroyer):
    def __init__(self, name="Russell", behavior=Destroyer.behavior_baseline, location=None, spawn_polygon=None):
        super().__init__(name, behavior, location, spawn_polygon)


class Perkins(Destroyer):
    def __init__(self, name="Perkins", behavior=Destroyer.behavior_baseline, location=None, spawn_polygon=None):
        super().__init__(name, behavior, location, spawn_polygon)


class Walke(Destroyer):
    def __init__(self, name="Walke", behavior=Destroyer.behavior_baseline, location=None, spawn_polygon=None):
        super().__init__(name, behavior, location, spawn_polygon)


class Sims(Destroyer):
    def __init__(self, name="Sims", behavior=Destroyer.behavior_baseline, location=None, spawn_polygon=None):
        super().__init__(name, behavior, location, spawn_polygon)


class Worden(Destroyer):
    def __init__(self, name="Worden", behavior=Destroyer.behavior_baseline, location=None, spawn_polygon=None):
        super().__init__(name, behavior, location, spawn_polygon)
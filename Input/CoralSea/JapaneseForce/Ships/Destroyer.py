# Author: Thomas C.F. Goolsby - tgoolsby@mit.edu
# This file was created in support of the CNCPT Thesis
# Fall 2020 - EM.THE

from CnCPT.Input.CoralSea.BaseClasses.Ship import Ship
from CnCPT.Input.CoralSea.UnitedStatesForce.Weapons.deck_gun import DeckGunAir, DeckGunSurface
from CnCPT.Simulation.UnitBehavior import BasicBehavior
from CnCPT.Simulation.Utility.SideEnum import SideEnum


class Destroyer(Ship):
    def __init__(self, name=None, behavior=None, location=None, spawn_polygon=None):
        super().__init__(name=name, behavior=behavior, location=location, spawn_polygon=spawn_polygon,
                         side=SideEnum.RED)
        self.cost = 200
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
        unit.kinematics.set_speed(10)
        BasicBehavior.RouteFollowing(unit, simulation_manager)


class Ariake(Destroyer):
    def __init__(self, name="Ariake", behavior=Destroyer.behavior_baseline, location=None, spawn_polygon=None):
        super().__init__(name, behavior, location, spawn_polygon)


class Yugure(Destroyer):
    def __init__(self, name="Yugure", behavior=Destroyer.behavior_baseline, location=None, spawn_polygon=None):
        super().__init__(name, behavior, location, spawn_polygon)


class Shigure(Destroyer):
    def __init__(self, name="Shigure", behavior=Destroyer.behavior_baseline, location=None, spawn_polygon=None):
        super().__init__(name, behavior, location, spawn_polygon)


class Shiratsuyu(Destroyer):
    def __init__(self, name="Shiratsuyu", behavior=Destroyer.behavior_baseline, location=None, spawn_polygon=None):
        super().__init__(name, behavior, location, spawn_polygon)


class Ushio(Destroyer):
    def __init__(self, name="Ushio", behavior=Destroyer.behavior_baseline, location=None, spawn_polygon=None):
        super().__init__(name, behavior, location, spawn_polygon)


class Akebono(Destroyer):
    def __init__(self, name="Akebono", behavior=Destroyer.behavior_baseline, location=None, spawn_polygon=None):
        super().__init__(name, behavior, location, spawn_polygon)


class Sazanami(Destroyer):
    def __init__(self, name="Sazanami", behavior=Destroyer.behavior_baseline, location=None, spawn_polygon=None):
        super().__init__(name, behavior, location, spawn_polygon)


class Oite(Destroyer):
    def __init__(self, name="Oite", behavior=Destroyer.behavior_baseline, location=None, spawn_polygon=None):
        super().__init__(name, behavior, location, spawn_polygon)


class Uzuki(Destroyer):
    def __init__(self, name="Uzuki", behavior=Destroyer.behavior_baseline, location=None, spawn_polygon=None):
        super().__init__(name, behavior, location, spawn_polygon)


class Asamagi(Destroyer):
    def __init__(self, name="Asamagi", behavior=Destroyer.behavior_baseline, location=None, spawn_polygon=None):
        super().__init__(name, behavior, location, spawn_polygon)


class Mutsuki(Destroyer):
    def __init__(self, name="Mutsuki", behavior=Destroyer.behavior_baseline, location=None, spawn_polygon=None):
        super().__init__(name, behavior, location, spawn_polygon)


class Yunagi(Destroyer):
    def __init__(self, name="Yunagi", behavior=Destroyer.behavior_baseline, location=None, spawn_polygon=None):
        super().__init__(name, behavior, location, spawn_polygon)


class Yayoi(Destroyer):
    def __init__(self, name="Yayoi", behavior=Destroyer.behavior_baseline, location=None, spawn_polygon=None):
        super().__init__(name, behavior, location, spawn_polygon)


class Okinoshima(Destroyer):
    def __init__(self, name="Okinoshima", behavior=Destroyer.behavior_baseline, location=None, spawn_polygon=None):
        super().__init__(name, behavior, location, spawn_polygon)


class KoeiMaru(Destroyer):
    def __init__(self, name="KoeiMaru", behavior=Destroyer.behavior_baseline, location=None, spawn_polygon=None):
        super().__init__(name, behavior, location, spawn_polygon)


class Kaikuzuki(Destroyer):
    def __init__(self, name="Kaikuzuki", behavior=Destroyer.behavior_baseline, location=None, spawn_polygon=None):
        super().__init__(name, behavior, location, spawn_polygon)


class Yuzuki(Destroyer):
    def __init__(self, name="Yuzuki", behavior=Destroyer.behavior_baseline, location=None, spawn_polygon=None):
        super().__init__(name, behavior, location, spawn_polygon)

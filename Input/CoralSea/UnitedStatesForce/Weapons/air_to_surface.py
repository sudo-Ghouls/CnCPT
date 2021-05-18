# Author: Thomas C.F. Goolsby - tgoolsby@mit.edu
# This file was created in support of the CNCPT Thesis
# Fall 2020 - EM.THE


from CnCPT.Input.CoralSea.BaseClasses.Ship import Ship
from CnCPT.Simulation.Weapons.Weapon import Weapon


class AirLaunchedBomb(Weapon):
    def __init__(self, name, amount):
        super().__init__(name, amount)
        self.pk = .3
        self.engagement_rate = 60  # in seconds
        self.max_range = 1000  # in meters
        self.viable_target_classes = Ship


class AirLaunchedTorpedo(Weapon):
    def __init__(self, name, amount):
        super().__init__(name, amount)
        self.pk = .5
        self.engagement_rate = 60  # in seconds
        self.max_range = 500  # in meters
        self.viable_target_classes = Ship

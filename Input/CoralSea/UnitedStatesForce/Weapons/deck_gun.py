# Author: Thomas C.F. Goolsby - tgoolsby@mit.edu
# This file was created in support of the CNCPT Thesis
# Fall 2020 - EM.THE


from Input.CoralSea.BaseClasses.Aircraft import Aircraft
from Input.CoralSea.BaseClasses.Ship import Ship
from Simulation.Engagement.Weapon import Weapon


class DeckGun(Weapon):
    def __init__(self, name, amount):
        super().__init__(name, amount)
        self.engagements_conducted = 0
        self.pk = .5
        self.engagement_rate = 60  # in seconds
        self.max_range = None  # in meters
        self.engagement_history_dict = {}
        self.viable_target_classes = (Aircraft, Ship)


class DeckGunSurface(DeckGun):
    def __init__(self, name, amount):
        super().__init__(name, amount)
        self.pk = .2
        self.engagement_rate = 300  # in seconds
        self.max_range = 30 * 1000  # in meters
        self.viable_target_classes = Ship


class DeckGunAir(DeckGun):
    def __init__(self, name, amount):
        super().__init__(name, amount)
        self.pk = .1
        self.engagement_rate = 60  # in seconds
        self.max_range = 5 * 1000  # in meters
        self.viable_target_classes = Aircraft

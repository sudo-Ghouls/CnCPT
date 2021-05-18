# Author: Thomas C.F. Goolsby - tgoolsby@mit.edu
# This file was created in support of the CNCPT Thesis
# Fall 2020 - EM.THE


from CnCPT.Input.CoralSea.BaseClasses.Aircraft import Aircraft
from CnCPT.Simulation.Weapons.Weapon import Weapon


class AirToAirGun(Weapon):
    def __init__(self, name, amount):
        super().__init__(name, amount)
        self.pk = .1
        self.engagement_rate = 30  # in seconds
        self.max_range = 500  # in meters
        self.viable_target_classes = Aircraft

# Author: Thomas C.F. Goolsby - tgoolsby@mit.edu
# This file was created in support of the CNCPT Thesis
# Fall 2020 - EM.THE

from CnCPT.Simulation.UnitBehavior import BasicBehavior
from CnCPT.Simulation.Units.Unit import Unit


class Ship(Unit):
    def __init__(self, name=None, behavior=None, location=None, spawn_polygon=None, side=None):
        super().__init__(name=name, behavior=behavior, location=location, spawn_polygon=spawn_polygon,
                         side=side)

    def my_brain(self, _self, simulation_manager):
        BasicBehavior.RouteFollowing(self, simulation_manager)

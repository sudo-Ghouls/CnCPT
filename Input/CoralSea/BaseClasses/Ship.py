# Author: Thomas C.F. Goolsby - tgoolsby@mit.edu
# This file was created in support of the CNCPT Thesis
# Fall 2020 - EM.THE

from Simulation.Units.Unit import Unit
from Simulation.Units.core import BasicBehavior


class Ship(Unit):
    def __init__(self, name=None, behavior=None, location=None, spawn_polygon=None,
                 side=None, route=None, parent=None, network=None, group_data=None):
        super().__init__(name=name, behavior=behavior, location=location, spawn_polygon=spawn_polygon,
                         side=side, route=route, parent=parent, network=network, group_data=group_data)

    def my_brain(self, _self, simulation_manager):
        BasicBehavior.RouteFollowing(self, simulation_manager)

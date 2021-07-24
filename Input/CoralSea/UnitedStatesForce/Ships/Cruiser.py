# Author: Thomas C.F. Goolsby - tgoolsby@mit.edu
# This file was created in support of the CNCPT Thesis
# Fall 2020 - EM.THE

from Simulation.Units.BaseClasses.Ship import Ship
from Input.CoralSea.UnitedStatesForce.Logic.CruiserLogic import behavior_baseline
from Input.CoralSea.UnitedStatesForce.Sensors.Visual import VisualSurface
from Input.CoralSea.UnitedStatesForce.Weapons.deck_gun import DeckGunAir, DeckGunSurface
from Simulation.Units.State import State
from Simulation.Utility.SideEnum import SideEnum


class Cruiser(Ship):
    def __init__(self, name=None, behavior=None, location=None, spawn_polygon=None,
                 side=SideEnum.BLUE, route=None, parent=None, network=None, group_data=None, kinematics_data=None):
        super().__init__(name=name, behavior=behavior, location=location, spawn_polygon=spawn_polygon,
                         side=side, route=route, parent=parent, network=network, group_data=group_data,
                         kinematics_data=kinematics_data)
        self.cost = 200
        self.add_sensor(VisualSurface())
        self.add_weapon(DeckGunAir, 1000)
        self.add_weapon(DeckGunSurface, 1000)
        self.state = State.PATROL


class AustralianCruiser(Cruiser):
    def __init__(self, name=None, behavior=None, location=None, spawn_polygon=None,
                 side=SideEnum.BLUE, route=None, parent=None, network=None, group_data=None, kinematics_data=None):
        super().__init__(name=name, behavior=behavior, location=location, spawn_polygon=spawn_polygon,
                         side=side, route=route, parent=parent, network=network, group_data=group_data,
                         kinematics_data=kinematics_data)
        self.cost = 200


class Minneapolis(Cruiser):
    def __init__(self, name="Minneapolis", behavior=behavior_baseline, location=None, spawn_polygon=None,
                 side=SideEnum.BLUE, route=None, parent=None, network=None, group_data=None, kinematics_data=None):
        super().__init__(name=name, behavior=behavior, location=location, spawn_polygon=spawn_polygon,
                         side=side, route=route, parent=parent, network=network, group_data=group_data,
                         kinematics_data=kinematics_data)


class NewOrleans(Cruiser):
    def __init__(self, name="NewOrleans", behavior=behavior_baseline, location=None, spawn_polygon=None,
                 side=SideEnum.BLUE, route=None, parent=None, network=None, group_data=None, kinematics_data=None):
        super().__init__(name=name, behavior=behavior, location=location, spawn_polygon=spawn_polygon,
                         side=side, route=route, parent=parent, network=network, group_data=group_data,
                         kinematics_data=kinematics_data)


class Astoria(Cruiser):
    def __init__(self, name="Astoria", behavior=behavior_baseline, location=None, spawn_polygon=None,
                 side=SideEnum.BLUE, route=None, parent=None, network=None, group_data=None, kinematics_data=None):
        super().__init__(name=name, behavior=behavior, location=location, spawn_polygon=spawn_polygon,
                         side=side, route=route, parent=parent, network=network, group_data=group_data,
                         kinematics_data=kinematics_data)


class Chester(Cruiser):
    def __init__(self, name="Chester", behavior=behavior_baseline, location=None, spawn_polygon=None,
                 side=SideEnum.BLUE, route=None, parent=None, network=None, group_data=None, kinematics_data=None):
        super().__init__(name=name, behavior=behavior, location=location, spawn_polygon=spawn_polygon,
                         side=side, route=route, parent=parent, network=network, group_data=group_data,
                         kinematics_data=kinematics_data)


class Portland(Cruiser):
    def __init__(self, name="Portland", behavior=behavior_baseline, location=None, spawn_polygon=None,
                 side=SideEnum.BLUE, route=None, parent=None, network=None, group_data=None, kinematics_data=None):
        super().__init__(name=name, behavior=behavior, location=location, spawn_polygon=spawn_polygon,
                         side=side, route=route, parent=parent, network=network, group_data=group_data,
                         kinematics_data=kinematics_data)


class Chicago(Cruiser):
    def __init__(self, name="Chicago", behavior=behavior_baseline, location=None, spawn_polygon=None,
                 side=SideEnum.BLUE, route=None, parent=None, network=None, group_data=None, kinematics_data=None):
        super().__init__(name=name, behavior=behavior, location=location, spawn_polygon=spawn_polygon,
                         side=side, route=route, parent=parent, network=network, group_data=group_data,
                         kinematics_data=kinematics_data)


class Australia(AustralianCruiser):
    def __init__(self, name="Australia", behavior=behavior_baseline, location=None, spawn_polygon=None,
                 side=SideEnum.BLUE, route=None, parent=None, network=None, group_data=None, kinematics_data=None):
        super().__init__(name=name, behavior=behavior, location=location, spawn_polygon=spawn_polygon,
                         side=side, route=route, parent=parent, network=network, group_data=group_data,
                         kinematics_data=kinematics_data)


class Hobart(AustralianCruiser):
    def __init__(self, name="Hobart", behavior=behavior_baseline, location=None, spawn_polygon=None,
                 side=SideEnum.BLUE, route=None, parent=None, network=None, group_data=None, kinematics_data=None):
        super().__init__(name=name, behavior=behavior, location=location, spawn_polygon=spawn_polygon,
                         side=side, route=route, parent=parent, network=network, group_data=group_data,
                         kinematics_data=kinematics_data)

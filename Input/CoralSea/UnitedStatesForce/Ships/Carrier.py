# Author: Thomas C.F. Goolsby - tgoolsby@mit.edu
# This file was created in support of the CNCPT Thesis
# Fall 2020 - EM.THE

from Input.CoralSea.BaseClasses.Ship import Ship
from Input.CoralSea.UnitedStatesForce.Aircraft.DiveBomber import DouglasSBDDauntless
from Input.CoralSea.UnitedStatesForce.Aircraft.Fighter import GrummanF4F3Wildcat
from Input.CoralSea.UnitedStatesForce.Aircraft.TorpedoBomber import DouglasTBDDevastator
from Input.CoralSea.UnitedStatesForce.Logic.CruiserLogic import behavior_baseline
from Input.CoralSea.UnitedStatesForce.Sensors.BasicRadarCXAM import BasicRadarCXAM
from Input.CoralSea.UnitedStatesForce.Sensors.Visual import VisualSurface
from Input.CoralSea.UnitedStatesForce.Weapons.deck_gun import DeckGunAir, DeckGunSurface
from Simulation.Utility.SideEnum import SideEnum
from Simulation.Units.State import State


class Carrier(Ship):
    def __init__(self, name=None, behavior=None, location=None, spawn_polygon=None,
                 side=SideEnum.BLUE, route=None, parent=None, network=None, group_data=None, kinematics_data=None):
        super().__init__(name=name, behavior=behavior, location=location, spawn_polygon=spawn_polygon,
                         side=side, route=route, parent=parent, network=network, group_data=group_data,
                         kinematics_data=kinematics_data)
        self.cost = 2000
        self.add_sensor(BasicRadarCXAM())
        self.add_sensor(VisualSurface())
        self.add_weapon(DeckGunAir, 1000)
        self.add_weapon(DeckGunSurface, 1000)
        self.state = State.PATROL
        self.my_carriers = None
        self.my_destroyers = None
        self.my_cruisers = None
        self.my_aircraft = None

        self.search_mission = None
        self.air_wing_mission = None

        # Enemy Info
        self.enemy_bearing = 0
        self.enemy_distance = 200
        self.target_located = False
        self.target_location = None

        if not hasattr(self, "aircraft"):
            self.aircraft = {DouglasSBDDauntless: 35,
                             GrummanF4F3Wildcat: 17,
                             DouglasTBDDevastator: 10}
            self.add_children(self.aircraft)


# US carrier aircraft numbers by ship the morning of 7 May: Lexington- 35 Douglas SBD Dauntless dive bombers, 12
# Douglas TBD Devastator torpedo bombers, 19 Grumman F4F-3 Wildcat fighters; Yorktown- 35 SBD, 10 TBD, 17 F4F-3
# (Lundstrom 2005b, p. 190).

class Yorktown(Carrier):
    def __init__(self, name="Yorktown", behavior=behavior_baseline, location=None, spawn_polygon=None,
                 side=SideEnum.BLUE, route=None, parent=None, network=None, group_data=None, kinematics_data=None):
        self.aircraft = {DouglasSBDDauntless: 35,
                         GrummanF4F3Wildcat: 17,
                         DouglasTBDDevastator: 10}
        super().__init__(name=name, behavior=behavior, location=location, spawn_polygon=spawn_polygon,
                         side=side, route=route, parent=parent, network=network, group_data=group_data,
                         kinematics_data=kinematics_data)
        self.add_children(self.aircraft)


class Lexington(Carrier):
    def __init__(self, name="Lexington", behavior=behavior_baseline, location=None, spawn_polygon=None,
                 side=SideEnum.BLUE, route=None, parent=None, network=None, group_data=None, kinematics_data=None):
        self.aircraft = {DouglasSBDDauntless: 35,
                         GrummanF4F3Wildcat: 19,
                         DouglasTBDDevastator: 12}
        super().__init__(name=name, behavior=behavior, location=location, spawn_polygon=spawn_polygon,
                         side=side, route=route, parent=parent, network=network, group_data=group_data,
                         kinematics_data=kinematics_data)
        self.add_children(self.aircraft)

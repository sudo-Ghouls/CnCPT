# Author: Thomas C.F. Goolsby - tgoolsby@mit.edu
# This file was created in support of the CNCPT Thesis
# Fall 2020 - EM.THE

import itertools

from CnCPT.Input.CoralSea.BaseClasses.Ship import Ship
from CnCPT.Input.CoralSea.UnitedStatesForce.Aircraft.DiveBomber import DouglasSBDDauntless
from CnCPT.Input.CoralSea.UnitedStatesForce.Aircraft.Fighter import GrummanF4F3Wildcat
from CnCPT.Input.CoralSea.UnitedStatesForce.Aircraft.TorpedoBomber import DouglasTBDDevastator
from CnCPT.Input.CoralSea.UnitedStatesForce.Sensors.BasicRadarCXAM import BasicRadarCXAM
from CnCPT.Input.CoralSea.UnitedStatesForce.Sensors.Visual import VisualSurface
from CnCPT.Input.CoralSea.UnitedStatesForce.Ships.Cruiser import Cruiser
from CnCPT.Input.CoralSea.UnitedStatesForce.Ships.Destroyer import Destroyer
from CnCPT.Input.CoralSea.UnitedStatesForce.Weapons.deck_gun import DeckGunAir, DeckGunSurface
from CnCPT.Simulation.GeographyPhysics import Geography
from CnCPT.Simulation.Units.State import State
from CnCPT.Simulation.Utility.Area import Area
from CnCPT.Simulation.Utility.Conversions import kts_to_ms
from CnCPT.Simulation.Utility.SideEnum import SideEnum


class Carrier(Ship):
    def __init__(self, name=None, behavior=None, location=None, spawn_polygon=None):
        super().__init__(name=name, behavior=behavior, location=location, spawn_polygon=spawn_polygon,
                         side=SideEnum.BLUE)
        self.cost = 200
        self.add_sensor(BasicRadarCXAM())
        self.add_sensor(VisualSurface())
        self.add_weapon(DeckGunAir, 1000)
        self.add_weapon(DeckGunSurface, 1000)
        self.my_carriers = None
        self.my_destroyers = None
        self.my_cruisers = None
        self.my_aircraft = None

        self.search_mission = None
        self.air_wing_mission = None

        # Enemy Info
        self.enemy_bearing = 0
        self.enemy_distance = 100
        self.target_located = False

    @staticmethod
    def behavior_aggressive(unit, simulation_manager):
        pass

    @staticmethod
    def behavior_passive(unit, simulation_manager):
        pass

    @staticmethod
    def behavior_startup(unit, simulation_manager):
        unit.my_carriers = [child for child in unit.group.units if isinstance(child, Carrier)]
        unit.my_destroyers = [child for child in unit.group.units if isinstance(child, Destroyer)]
        unit.my_cruisers = [child for child in unit.group.units if isinstance(child, Cruiser)]
        unit.my_aircraft = [child for child in
                            itertools.chain.from_iterable([carrier.children for carrier in unit.my_carriers]) if
                            isinstance(child, (DouglasSBDDauntless, GrummanF4F3Wildcat, DouglasTBDDevastator))]

        unit.brain = unit.behavior_baseline

    @staticmethod
    def behavior_baseline(unit, simulation_manager):
        if unit.group.leader is unit:
            # Morning Op
            if unit.search_mission is None:
                unit.deploy_search_mission(unit.enemy_bearing, unit.enemy_distance,
                                           DouglasSBDDauntless, 10, simulation_manager.now)

            if unit.target_located is True:
                air_wing_composition = {DouglasSBDDauntless: 35,
                                        GrummanF4F3Wildcat: 17,
                                        DouglasTBDDevastator: 10}
                unit.deploy_carrier_air_wing(unit.enemy_bearing, unit.enemy_distance, air_wing_composition,
                                             simulation_manager.now)

            # 06:19 - Believing Takagi's carrier force was somewhere north of him, in the vicinity of the Louisiades,
            # beginning at 06:19, Fletcher directed Yorktown to send 10 Douglas SBD Dauntless dive bombers as scouts to
            # search that area.

            # 06:25 -  on 7 May, TF 17 was 115 nmi (132 mi; 213 km) south of Rossel Island (13°20′S 154°21′E). At this
            # time, Fletcher sent Crace's cruiser force, now designated Task Group 17.3 (TG 17.3), to block the Jomard
            # Passage. Fletcher understood that Crace would be operating without air cover since TF 17's carriers would
            # be busy trying to locate and attack the Japanese carriers. Detaching Crace reduced the anti-aircraft defenses
            # for Fletcher's carriers. Nevertheless, Fletcher decided the risk was necessary to ensure the Japanese invasion
            # forces could not slip through to Port Moresby while he engaged the carriers.[43]

            # 08:15 -  a Yorktown SBD piloted by John L. Nielsen sighted Gotō's force screening the invasion convoy.

            # 10:12 -  Fletcher received a report of an aircraft carrier, ten transports, and 16 warships 30 nmi
            # (35 mi; 56 km) south of Nielsen's sighting at 10°35′S 152°36′E. The B-17s actually saw the same thing as
            # Nielsen: Shōhō, Gotō's cruisers, plus the Port Moresby Invasion Force.

            # 10:13 -  the U.S. strike of 93 aircraft—18 Grumman F4F Wildcats, 53 Douglas SBD Dauntless dive bombers,
            # and 22 Douglas TBD Devastator torpedo bombers—was on its way

            # 10:40 - The U.S. strike aircraft sighted Shōhō a short distance northeast of Misima Island at 10:40 and
            # deployed to attack.
        unit.kinematics.set_speed(kts_to_ms(30))

    def deploy_search_mission(self, bearing, distance, aircraft_type, aircraft_number, time):
        carrier_location = self.kinematics.get_location()
        center = Geography.reckon(distance, bearing, carrier_location[0], carrier_location[1], unit="nmi")
        patrol_area = Area.create_patrol_area_from_center(center, 100, 100, unit='nmi')
        docked_aircraft = [aircraft for aircraft in self.my_aircraft if
                           aircraft.state is State.DOCKED and isinstance(aircraft, aircraft_type)]

        for i in range(aircraft_number):
            docked_aircraft[i].state = State.SEARCH
            docked_aircraft[i].state_change_time = time
            docked_aircraft[i].formation_lock = False
            docked_aircraft[i].area = patrol_area
            docked_aircraft[i].kinematics.set_heading(bearing)
            docked_aircraft[i].kinematics.set_speed(docked_aircraft[i].kinematics._max_speed/2)

        self.search_mission = True

    def deploy_carrier_air_wing(self, bearing, distance, air_wing_composition, time):
        pass


# US carrier aircraft numbers by ship the morning of 7 May: Lexington- 35 Douglas SBD Dauntless dive bombers, 12
# Douglas TBD Devastator torpedo bombers, 19 Grumman F4F-3 Wildcat fighters; Yorktown- 35 SBD, 10 TBD, 17 F4F-3
# (Lundstrom 2005b, p. 190).

class Yorktown(Carrier):
    def __init__(self, name="Yorktown", behavior=Carrier.behavior_startup, location=None, spawn_polygon=None):
        super().__init__(name, behavior, location, spawn_polygon)
        self.aircraft = {DouglasSBDDauntless: 35,
                         GrummanF4F3Wildcat: 17,
                         DouglasTBDDevastator: 10}
        self.add_children(self.aircraft)


class Lexington(Carrier):
    def __init__(self, name="Lexington", behavior=Carrier.behavior_startup, location=None, spawn_polygon=None):
        super().__init__(name, behavior, location, spawn_polygon)
        self.aircraft = {DouglasSBDDauntless: 35,
                         GrummanF4F3Wildcat: 19,
                         DouglasTBDDevastator: 12}
        self.add_children(self.aircraft)

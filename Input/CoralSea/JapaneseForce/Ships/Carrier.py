# Author: Thomas C.F. Goolsby - tgoolsby@mit.edu
# This file was created in support of the CNCPT Thesis
# Fall 2020 - EM.THE

import itertools

from Input.CoralSea.BaseClasses.Ship import Ship
from Input.CoralSea.JapaneseForce.Aircraft.DiveBomber import AichiD3AType99
from Input.CoralSea.JapaneseForce.Aircraft.Fighter import A6M2Zero
from Input.CoralSea.JapaneseForce.Aircraft.TorpedoBomber import NakajimaB5NType97
from Input.CoralSea.JapaneseForce.Sensors.Visual import VisualSurface
from Input.CoralSea.JapaneseForce.Ships.Destroyer import Destroyer
from Input.CoralSea.JapaneseForce.Ships.Gunboat import Gunboat
from Input.CoralSea.JapaneseForce.Ships.HeavyCruiser import HeavyCruiser
from Input.CoralSea.JapaneseForce.Ships.LightCarrier import LightCarrier
from Input.CoralSea.JapaneseForce.Ships.LightCrusier import LightCruiser
from Input.CoralSea.JapaneseForce.Ships.Minelayer import Minelayer
from Input.CoralSea.JapaneseForce.Ships.Tanker import Tanker
from Input.CoralSea.JapaneseForce.Ships.Transport import Transport
from Input.CoralSea.JapaneseForce.Weapons.deck_gun import DeckGunAir, DeckGunSurface
from Simulation.GeographyPhysics.core import bearing, reckon
from Simulation.Logic.ChildLogic import undock
from Simulation.Logic.General import is_day
from Simulation.Units.State import State
from Simulation.Utility.Area import Area
from Simulation.Utility.Conversions import kts_to_ms
from Simulation.Utility.SideEnum import SideEnum


class Carrier(Ship):
    def __init__(self, name=None, behavior=None, location=None, spawn_polygon=None, side=SideEnum.RED, route=None,
                 parent=None, network=None, group_data=None, kinematics_data=None):
        super().__init__(name=name, behavior=behavior, location=location, spawn_polygon=spawn_polygon,
                         side=side, route=route, parent=parent, network=network, group_data=group_data,
                         kinematics_data=kinematics_data)
        self.cost = 2000
        self.add_sensor(VisualSurface())
        self.add_weapon(DeckGunAir, 1000)
        self.add_weapon(DeckGunSurface, 1000)
        self.my_carriers = None
        self.my_destroyers = None
        self.my_LightCarriers = None
        self.my_LightCruisers = None
        self.my_HeavyCruisers = None
        self.my_Gunboats = None
        self.my_Minelayers = None
        self.my_Tankers = None
        self.my_Transports = None
        self.my_aircraft = None

        self.search_mission = None
        self.air_wing_mission = None

        # Enemy Info
        self.enemy_bearing = 180
        self.enemy_distance = 200
        self.target_located = False
        self.target_location = None

    @staticmethod
    def behavior_startup(unit, simulation_manager):
        unit.my_carriers = [child for child in unit.group.units if isinstance(child, Carrier)]
        unit.my_destroyers = [child for child in unit.group.units if isinstance(child, Destroyer)]
        unit.my_LightCarriers = [child for child in unit.group.units if isinstance(child, LightCarrier)]
        unit.my_LightCruisers = [child for child in unit.group.units if isinstance(child, LightCruiser)]
        unit.my_HeavyCruisers = [child for child in unit.group.units if isinstance(child, HeavyCruiser)]
        unit.my_Gunboats = [child for child in unit.group.units if isinstance(child, Gunboat)]
        unit.my_Minelayers = [child for child in unit.group.units if isinstance(child, Minelayer)]
        unit.my_Tankers = [child for child in unit.group.units if isinstance(child, Tanker)]
        unit.my_Transports = [child for child in unit.group.units if isinstance(child, Transport)]

        all_carriers = unit.my_carriers + unit.my_LightCarriers
        unit.my_aircraft = [child for child in
                            itertools.chain.from_iterable([carrier.children for carrier in all_carriers]) if
                            isinstance(child, (AichiD3AType99, A6M2Zero, NakajimaB5NType97))]

        unit.brain = unit.behavior_baseline

    @staticmethod
    def behavior_baseline(unit, simulation_manager):
        if unit.group.leader is unit:
            # Morning Op
            if is_day(simulation_manager.now):
                if unit.search_mission is None:
                    unit.deploy_search_mission(unit.enemy_bearing, unit.enemy_distance,
                                               NakajimaB5NType97, 10, simulation_manager.now)
                else:
                    search_aircraft = [aircraft for aircraft in unit.my_aircraft if
                                       aircraft.state is State.SEARCH and aircraft.alive]
                    if len(search_aircraft) < 10:
                        unit.search_mission = None

                if unit.target_located is True and unit.air_wing_mission is None:
                    air_wing_composition = {AichiD3AType99: 35,
                                            A6M2Zero: 17,
                                            NakajimaB5NType97: 10}
                    unit.deploy_carrier_air_wing(unit.target_location, air_wing_composition,
                                                 simulation_manager.now)
                else:
                    air_wing_aircraft = [aircraft for aircraft in unit.my_aircraft if
                                         aircraft.state is State.ENGAGE and aircraft.alive]
                    if len(air_wing_aircraft) < 10:
                        unit.air_wing_mission = None

        unit.kinematics.set_speed(kts_to_ms(10))

    def deploy_search_mission(self, bearing_to, distance, aircraft_type, aircraft_number, time):
        carrier_location = self.kinematics.get_location()
        center = reckon(distance, bearing_to, carrier_location[0], carrier_location[1], unit="nmi")
        patrol_area = Area.create_patrol_area_from_center(center, 100, 100, unit='nmi')
        docked_aircraft = [aircraft for aircraft in self.my_aircraft if
                           aircraft.state is State.DOCKED_READY and isinstance(aircraft, aircraft_type)]
        try:
            for i in range(aircraft_number):
                undock(docked_aircraft[i], State.SEARCH, time)
                docked_aircraft[i].area = patrol_area
                docked_aircraft[i].kinematics.set_heading(bearing_to)
                docked_aircraft[i].kinematics.set_speed(docked_aircraft[i].kinematics._max_speed / 2)
        except IndexError:
            pass

        self.search_mission = True

    def deploy_carrier_air_wing(self, target_location, air_wing_composition, time):
        carrier_location = self.kinematics.get_location()
        patrol_area = Area.create_patrol_area_from_center(target_location, 50, 50, unit='nmi')
        bearing_to = bearing(carrier_location, target_location)
        for aircraft_type in air_wing_composition:
            docked_aircraft = [aircraft for aircraft in self.my_aircraft if
                               aircraft.state is State.DOCKED_READY and isinstance(aircraft, aircraft_type)]
            try:
                for i in range(air_wing_composition[aircraft_type]):
                    undock(docked_aircraft[i], State.ENGAGE, time)
                    docked_aircraft[i].area = patrol_area
                    docked_aircraft[i].kinematics.set_heading(bearing_to)
                    docked_aircraft[i].kinematics.set_speed(docked_aircraft[i].kinematics._max_speed / 2)
            except IndexError:
                pass

        self.air_wing_mission = True


#  Shōkaku 58 total - 21 Aichi D3A Type 99 "kanbaku" dive bombers, 19 Nakajima B5N Type 97 "kankō" torpedo bombers,
#  18 A6M2 Zero fighters; Zuikaku 63 total - 21 kankō, 22 kanbaku, 20 Zeros; Shōhō 18 total - 6 kankō, 4 Mitsubishi
#  A5M Type 96 fighters, 8 Zeros (Lundstrom 2005b, p. 188; Millot 1974, p. 154). Cressman 2000, p. 93, states Shōhō
#  carried 13 fighters without specifying how many of which type. (Lundstrom 2005b, p. 188; Millot 1974, p. 154).

class Shokaku(Carrier):
    def __init__(self, name="Shokaku", behavior=Carrier.behavior_startup, location=None, spawn_polygon=None,
                 side=SideEnum.RED, route=None, parent=None, network=None, group_data=None, kinematics_data=None):
        super().__init__(name=name, behavior=behavior, location=location, spawn_polygon=spawn_polygon,
                         side=side, route=route, parent=parent, network=network, group_data=group_data,
                         kinematics_data=kinematics_data)
        self.aircraft = {AichiD3AType99: 21,
                         NakajimaB5NType97: 19,
                         A6M2Zero: 18}
        self.add_children(self.aircraft)


class Zuikaku(Carrier):
    def __init__(self, name="Zuikaku", behavior=Carrier.behavior_startup, location=None, spawn_polygon=None,
                 side=SideEnum.RED, route=None, parent=None, network=None, group_data=None, kinematics_data=None):
        super().__init__(name=name, behavior=behavior, location=location, spawn_polygon=spawn_polygon,
                         side=side, route=route, parent=parent, network=network, group_data=group_data,
                         kinematics_data=kinematics_data)
        self.aircraft = {AichiD3AType99: 22,
                         NakajimaB5NType97: 21,
                         A6M2Zero: 20}
        self.add_children(self.aircraft)

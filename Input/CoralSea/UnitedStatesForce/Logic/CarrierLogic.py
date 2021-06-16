# Author: Thomas C.F. Goolsby - tgoolsby@mit.edu
# This file was created in support of the CNCPT Thesis
# Fall 2020 - EM.THE

import itertools

from Input.CoralSea.UnitedStatesForce.Aircraft.DiveBomber import DouglasSBDDauntless
from Input.CoralSea.UnitedStatesForce.Aircraft.Fighter import GrummanF4F3Wildcat
from Input.CoralSea.UnitedStatesForce.Aircraft.TorpedoBomber import DouglasTBDDevastator
from Input.CoralSea.UnitedStatesForce.Ships.Cruiser import Cruiser
from Input.CoralSea.UnitedStatesForce.Ships.Destroyer import Destroyer
from Simulation.GeographyPhysics.core import bearing, reckon
from Simulation.Logic.ChildLogic import undock
from Simulation.Logic.General import is_day
from Simulation.Logic.Patrol import patrol
from Simulation.Units.State import State
from Simulation.Utility.Area import Area
from Simulation.Utility.Conversions import kts_to_ms


def behavior_aggressive(unit, simulation_manager):
    unit.my_carriers = [child for child in unit.group.units if isinstance(child, unit.__class__)]
    unit.my_destroyers = [child for child in unit.group.units if isinstance(child, Destroyer)]
    unit.my_cruisers = [child for child in unit.group.units if isinstance(child, Cruiser)]
    unit.my_aircraft = [child for child in
                        itertools.chain.from_iterable([carrier.children for carrier in unit.my_carriers]) if
                        isinstance(child, (DouglasSBDDauntless, GrummanF4F3Wildcat, DouglasTBDDevastator))]
    if unit.area is None and unit.route is None:
        # establish patrol area 150 miles into enemy territory
        my_location = unit.kinematics.get_location()
        center = reckon(150, 0, my_location[0], my_location[1], unit="nmi")
        unit.area = Area.create_patrol_area_from_center(center, 100, 100, unit='nmi')
    unit.brain = behavior_aggressive_core


def behavior_aggressive_core(unit, simulation_manager):
    """This behavior aggressively search dispatching 10 search aircraft on 18 degree bearings from 270 to 90 degrees
    once the enemy is detected all available aircraft are sent towards the enemy

    """
    if unit.group.leader is unit:
        if is_day(simulation_manager.now):
            if unit.search_mission is None:
                deploy_search_mission(unit, -90, 0, DouglasSBDDauntless, 2, simulation_manager.now, append_search=True)

            elif len(unit.search_mission) < 10:
                bearing = -90 + (len(unit.search_mission) + 1) * 18
                deploy_search_mission(unit, bearing, 0, DouglasSBDDauntless, 2, simulation_manager.now, append_search=True)
            else:
                search_aircraft = [aircraft for aircraft in unit.my_aircraft if
                                   aircraft.state is State.SEARCH and aircraft.alive]
                if len(search_aircraft) < 2:
                    unit.search_mission = None

            if unit.target_located is True and unit.air_wing_mission is None:
                air_wing_composition = {DouglasSBDDauntless: True,
                                        GrummanF4F3Wildcat: True,
                                        DouglasTBDDevastator: True}
                deploy_carrier_air_wing(unit, unit.target_location, air_wing_composition,
                                        simulation_manager.now)
            else:
                air_wing_aircraft = [aircraft for aircraft in unit.my_aircraft if
                                     aircraft.state is State.ENGAGE and aircraft.alive]
                if len(air_wing_aircraft) < 10:
                    unit.air_wing_mission = None
        if unit.route is None:
            patrol(unit)


def behavior_passive(unit, simulation_manager):
    unit.my_carriers = [child for child in unit.group.units if isinstance(child, unit.__class__)]
    unit.my_destroyers = [child for child in unit.group.units if isinstance(child, Destroyer)]
    unit.my_cruisers = [child for child in unit.group.units if isinstance(child, Cruiser)]
    unit.my_aircraft = [child for child in
                        itertools.chain.from_iterable([carrier.children for carrier in unit.my_carriers]) if
                        isinstance(child, (DouglasSBDDauntless, GrummanF4F3Wildcat, DouglasTBDDevastator))]
    if unit.area is None and unit.route is None:
        # establish patrol area 150 miles into enemy territory
        my_location = unit.kinematics.get_location()
        center = reckon(100, 180, my_location[0], my_location[1], unit="nmi")
        unit.area = Area.create_patrol_area_from_center(center, 100, 100, unit='nmi')
    unit.brain = behavior_passive_core


def behavior_passive_core(unit, simulation_manager):
    """This behavior places search aircraft around the carrier and only sends small air wings toward any enemy's
     detected.
    """
    if unit.group.leader is unit:
        if is_day(simulation_manager.now):
            if unit.search_mission is None:
                deploy_search_mission(unit, 0, 0, DouglasSBDDauntless, 2, simulation_manager.now)
            else:
                search_aircraft = [aircraft for aircraft in unit.my_aircraft if
                                   aircraft.state is State.SEARCH and aircraft.alive]
                if len(search_aircraft) < 2:
                    unit.search_mission = None

            if unit.target_located is True and unit.air_wing_mission is None:
                air_wing_composition = {DouglasSBDDauntless: 10,
                                        GrummanF4F3Wildcat: 10,
                                        DouglasTBDDevastator: 10}
                deploy_carrier_air_wing(unit, unit.target_location, air_wing_composition,
                                        simulation_manager.now)
            else:
                air_wing_aircraft = [aircraft for aircraft in unit.my_aircraft if
                                     aircraft.state is State.ENGAGE and aircraft.alive]
                if len(air_wing_aircraft) < 10:
                    unit.air_wing_mission = None
        if unit.route is None:
            patrol(unit)


def behavior_baseline(unit, simulation_manager):
    unit.my_carriers = [child for child in unit.group.units if isinstance(child, unit.__class__)]
    unit.my_destroyers = [child for child in unit.group.units if isinstance(child, Destroyer)]
    unit.my_cruisers = [child for child in unit.group.units if isinstance(child, Cruiser)]
    unit.my_aircraft = [child for child in
                        itertools.chain.from_iterable([carrier.children for carrier in unit.my_carriers]) if
                        isinstance(child, (DouglasSBDDauntless, GrummanF4F3Wildcat, DouglasTBDDevastator))]
    if unit.area is None and unit.route is None:
        # establish patrol area 150 miles into enemy territory
        my_location = unit.kinematics.get_location()
        unit.area = Area.create_patrol_area_from_center((my_location[0], my_location[1]), 100, 100, unit='nmi')
    unit.brain = behavior_baseline_core


def behavior_baseline_core(unit, simulation_manager):
    if unit.group.leader is unit:
        if is_day(simulation_manager.now):
            if unit.search_mission is None:
                deploy_search_mission(unit, unit.enemy_bearing, unit.enemy_distance,
                                      DouglasSBDDauntless, 10, simulation_manager.now)
            else:
                search_aircraft = [aircraft for aircraft in unit.my_aircraft if
                                   aircraft.state is State.SEARCH and aircraft.alive]
                if len(search_aircraft) < 10:
                    unit.search_mission = None

            if unit.target_located is True and unit.air_wing_mission is None:
                air_wing_composition = {DouglasSBDDauntless: 35,
                                        GrummanF4F3Wildcat: 17,
                                        DouglasTBDDevastator: 10}
                deploy_carrier_air_wing(unit, unit.target_location, air_wing_composition,
                                        simulation_manager.now)
            else:
                air_wing_aircraft = [aircraft for aircraft in unit.my_aircraft if
                                     aircraft.state is State.ENGAGE and aircraft.alive]
                if len(air_wing_aircraft) < 10:
                    unit.air_wing_mission = None
        if unit.route is None:
            patrol(unit)

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


def deploy_search_mission(unit, bearing, distance, aircraft_type, aircraft_number, time, append_search=False):
    carrier_location = unit.kinematics.get_location()
    center = reckon(distance, bearing, carrier_location[0], carrier_location[1], unit="nmi")
    patrol_area = Area.create_patrol_area_from_center(center, 100, 100, unit='nmi')
    docked_aircraft = [aircraft for aircraft in unit.my_aircraft if
                       aircraft.state is State.DOCKED_READY and isinstance(aircraft, aircraft_type)]
    try:
        for i in range(aircraft_number):
            undock(docked_aircraft[i], State.SEARCH, time)
            docked_aircraft[i].area = patrol_area
            docked_aircraft[i].kinematics.set_heading(bearing)
            docked_aircraft[i].kinematics.set_speed(docked_aircraft[i].kinematics._max_speed / 2)
    except IndexError:
        pass

    if not append_search:
        unit.search_mission = True
    else:
        if type(unit.search_mission) is list:
            unit.search_mission.append(True)
        else:
            unit.search_mission = [True]


def deploy_carrier_air_wing(unit, target_location, air_wing_composition, time):
    carrier_location = unit.kinematics.get_location()
    patrol_area = Area.create_patrol_area_from_center(target_location, 50, 50, unit='nmi')
    bearing_to = bearing(carrier_location, target_location)
    for aircraft_type in air_wing_composition:
        docked_aircraft = [aircraft for aircraft in unit.my_aircraft if
                           aircraft.state is State.DOCKED_READY and isinstance(aircraft, aircraft_type)]
        try:
            if type(air_wing_composition[aircraft_type]) is bool:
                if air_wing_composition[aircraft_type]:  # if true this will send everything we have
                    for i in range(len(docked_aircraft)):
                        undock(docked_aircraft[i], State.ENGAGE, time)
                        docked_aircraft[i].area = patrol_area
                        docked_aircraft[i].kinematics.set_heading(bearing_to)
                        docked_aircraft[i].kinematics.set_speed(docked_aircraft[i].kinematics._max_speed / 2)
            else:
                for i in range(air_wing_composition[aircraft_type]):
                    undock(docked_aircraft[i], State.ENGAGE, time)
                    docked_aircraft[i].area = patrol_area
                    docked_aircraft[i].kinematics.set_heading(bearing_to)
                    docked_aircraft[i].kinematics.set_speed(docked_aircraft[i].kinematics._max_speed / 2)
        except IndexError:
            pass

    unit.air_wing_mission = True
